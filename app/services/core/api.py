import typing as t
from enum import Enum
import time
import requests
import logging
from abc import ABC, abstractmethod

from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout, ConnectionError
from urllib3.util.retry import Retry

from app.utils.api import ApiError
from app.core.logging import logger


# Define ApiRoute as a TypeVar that must be an Enum
ApiRoute = t.TypeVar("ApiRoute", bound=Enum)


class BaseAPIService(ABC, t.Generic[ApiRoute]):
    """
    Abstract base class for all API services.
    Defines the interface that all API services must implement.
    
    Type Parameters:
        ApiRoute: An Enum type that defines the API routes for a specific service
    """

    @abstractmethod
    def get(self, url: ApiRoute, params: dict | None = None) -> dict:
        """Make a GET request to the API"""
        pass

    @abstractmethod
    def post(self, url: ApiRoute, data: dict | None = None) -> dict:
        """Make a POST request to the API"""
        pass

    @abstractmethod
    def put(self, url: ApiRoute, data: dict | None = None) -> dict:
        """Make a PUT request to the API"""
        pass

    @abstractmethod
    def delete(self, url: ApiRoute, params: dict | None = None) -> dict:
        """Make a DELETE request to the API"""
        pass

    @abstractmethod
    def patch(self, url: ApiRoute, data: dict | None = None) -> dict:
        """Make a PATCH request to the API"""
        pass

    @abstractmethod
    def set_auth_token(self, token: str) -> None:
        """Set authentication token for requests"""
        pass

    @abstractmethod
    def clear_auth_token(self) -> None:
        """Clear authentication token"""
        pass


class APIService(BaseAPIService[ApiRoute]):
    """
    Concrete implementation of API service with common functionality.
    Provides a robust implementation with rate limiting, retries, and error handling.
    
    Type Parameters:
        ApiRoute: An Enum type that defines the API routes for a specific service
    """
    
    def __init__(
        self, 
        service_name: str, 
        base_url: ApiRoute,
        headers: dict | None = None, 
        max_requests_per_minute: int = 60,
        retry_attempts: int = 5,
        retry_backoff_factor: float = 1.0,
        retry_status_codes: t.List[int] = [429, 500, 502, 503, 504]
    ):
        """
        Initialize the API service
        
        Args:
            service_name: Name of the service for logging
            base_url: Base URL for the API
            headers: Default headers for all requests
            max_requests_per_minute: Maximum number of requests allowed per minute
            retry_attempts: Number of retry attempts for failed requests
            retry_backoff_factor: Backoff factor between retries
            retry_status_codes: HTTP status codes that should trigger a retry
        """
        self.service_name = service_name
        self.base_url = base_url.value  # Access the Enum value
        self.headers = headers or {}
        self.max_requests_per_minute = max_requests_per_minute
        self.retry_config = {
            "attempts": retry_attempts,
            "backoff_factor": retry_backoff_factor,
            "status_codes": retry_status_codes
        }
        
        # Rate limiting state
        self.request_count = 0
        self.last_request_time = 0

        # Initialize session with retries
        self.session = self._create_session()
        logger.debug(f"Initialized {service_name} API service with base URL: {base_url.value}")

    def _create_session(self) -> requests.Session:
        """Create and configure a requests session with retries"""
        session = requests.Session()
        session.headers.update(self.headers)
        
        retries = Retry(
            total=self.retry_config["attempts"],
            backoff_factor=self.retry_config["backoff_factor"],
            status_forcelist=self.retry_config["status_codes"],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        logger.debug(f"Configured retry mechanism for {self.service_name}")
        return session

    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting"""
        now = time.time()
        time_window = 60  # 1 minute window

        if now - self.last_request_time > time_window:
            self.request_count = 0
            self.last_request_time = now

        if self.request_count >= self.max_requests_per_minute:
            wait_time = self.last_request_time + time_window - now
            logger.warning(f"Rate limit exceeded for {self.service_name}. Waiting {wait_time:.2f} seconds")
            raise ApiError("RATE_LIMIT_EXCEEDED", "Rate limit exceeded", {"retry_after": wait_time})

        self.request_count += 1
        self.last_request_time = now

    def _handle_http_error(self, error: RequestException) -> ApiError:
        """
        Handle HTTP errors and return appropriate ApiError
        
        Args:
            error: The request exception that occurred
            
        Returns:
            An ApiError instance with appropriate error details
        """
        if isinstance(error, Timeout):
            logger.error(f"Request timeout for {self.service_name}")
            return ApiError("TIMEOUT", "Request timed out")
            
        if isinstance(error, ConnectionError):
            logger.error(f"Connection error for {self.service_name}")
            return ApiError("CONNECTION_ERROR", "Connection error")
            
        if error.response:
            status = error.response.status_code
            error_mapping = {
                429: ("RATE_LIMIT_EXCEEDED", "Rate limit exceeded", {"retry_after": error.response.headers.get("Retry-After", "60")}),
                401: ("UNAUTHORIZED", "Unauthorized"),
                403: ("FORBIDDEN", "Forbidden"),
                404: ("NOT_FOUND", "Resource not found"),
            }
            
            if status in error_mapping:
                code, message, *extra = error_mapping[status]
                logger.warning(f"{message} for {self.service_name}")
                return ApiError(code, message, *extra)
                
            if status >= 500:
                logger.error(f"Server error for {self.service_name}: {status}")
                return ApiError("SERVER_ERROR", "Internal server error")
                
        logger.error(f"Unknown error for {self.service_name}: {str(error)}")
        return ApiError("UNKNOWN_ERROR", "An unexpected error occurred")

    def _make_request(self, method: str, url: ApiRoute, **kwargs) -> dict:
        """
        Make an HTTP request with rate limiting and error handling
        
        Args:
            method: HTTP method to use
            url: API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data as dictionary
        """
        self._check_rate_limit()
        try:
            full_url = f"{self.base_url}{url.value}"
            logger.debug(f"Making {method} request to {full_url}")
            response = self.session.request(
                method=method,
                url=full_url,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            raise self._handle_http_error(error)

    def get(self, url: ApiRoute, params: dict | None = None) -> dict:
        """Make a GET request to the API"""
        return self._make_request("GET", url, params=params)

    def post(self, url: ApiRoute, data: dict | None = None) -> dict:
        """Make a POST request to the API"""
        return self._make_request("POST", url, json=data)

    def put(self, url: ApiRoute, data: dict | None = None) -> dict:
        """Make a PUT request to the API"""
        return self._make_request("PUT", url, json=data)

    def delete(self, url: ApiRoute, params: dict | None = None) -> dict:
        """Make a DELETE request to the API"""
        return self._make_request("DELETE", url, params=params)

    def patch(self, url: ApiRoute, data: dict | None = None) -> dict:
        """Make a PATCH request to the API"""
        return self._make_request("PATCH", url, json=data)

    def set_auth_token(self, token: str) -> None:
        """Set authentication token for requests"""
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            logger.info(f"Auth token set for {self.service_name}")

    def clear_auth_token(self) -> None:
        """Clear authentication token"""
        self.session.headers.pop("Authorization", None)
        logger.info(f"Auth token cleared for {self.service_name}") 