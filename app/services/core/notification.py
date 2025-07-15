import typing as t
from abc import ABC, abstractmethod


class BaseNotificationService(ABC):
    """
    Abstract base class for all notification services
    """

    @abstractmethod
    def send_notification(self, message: str) -> None:
        """
        Send a notification
        """
        pass
