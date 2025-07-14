import typing as t

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Config(BaseSettings):
    # Details
    APP_NAME: str = "Cracked Trading Bot"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "An AI-powered crypto trading bot that runs on Believe tokens where it analyzes the token creator's (founder of the project) posts, and makes real-time buy decisions - all reported on Telegram."
    BOT_DESCRIPTION: str = "I am an AI-powered crypto trading bot that runs on Believe tokens where it analyzes the token creator's (founder of the project) posts, and makes real-time buy decisions - all reported on Telegram."

    # Application Configuration
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    # BOT_TOKEN: str
    LOGS_DIR: str = "logs"

    # Scheduler Configuration
    LAUNCHCOIN_SCHEDULER_RUN_ON_STARTUP: bool = False
    LAUNCHCOIN_SCHEDULER_INTERVAL: int = 60 * 15 # 15 minutes

    CREATOR_SCHEDULER_RUN_ON_STARTUP: bool = True
    CREATOR_SCHEDULER_INTERVAL: int = 60 * 5 # 5 minutes

    # Backend Configuration
    TWEET_SCRAPE_SERVICE_URL: str # URL of my own personal tweet scrape service

    COMPOSIO_API_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate that log level is a valid logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v


config = Config()
