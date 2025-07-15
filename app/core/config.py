import typing as t

from pydantic_settings import BaseSettings
from pydantic import field_validator
from app.static.tokens import SolanaNetworks


class Config(BaseSettings):
    # Details
    APP_NAME: str = "Cracked Trading Bot"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Believe X AI-powered personal crypto trading bot that runs 24/7 on Believe tokens, analyzing token creators' posts and making real-time buy/sell decisions - all reported via Telegram."
    BOT_DESCRIPTION: str = "I am an AI-powered personal crypto trading bot that runs 24/7 on Believe tokens, analyzing token creators' posts and making real-time buy/sell decisions - all reported via Telegram."

    # Application Configuration
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    BOT_TOKEN: str
    TELEGRAM_CHAT_ID: int = 5611375328 # Telegram ID of the user who will be receiving the trading decisions.
    LOGS_DIR: str = "logs"

    # Scheduler Configuration
    LAUNCHCOIN_SCHEDULER_RUN_ON_STARTUP: bool = False
    LAUNCHCOIN_SCHEDULER_INTERVAL: int = 60 * 15 # 15 minutes

    CREATOR_SCHEDULER_RUN_ON_STARTUP: bool = True
    CREATOR_SCHEDULER_INTERVAL: int = 60 * 5 # 5 minutes

    # Trading Agent Configuration
    TRADING_AGENT_TYPE: t.Literal["chill", "aggressive", "moderate"] = "chill" # "chill" or "aggressive" or "moderate"
    AUTONOMOUS_TRADING: bool = False # If True, the trading agent will make decisions and do trading on its own. If False, the trading agent will wait for confirmation from the user.
    TRADING_AGENT_MODEL: str = "gpt-4o" # NOTE: Currently, only gpt-4o is supported.
    PRIVATE_KEY: str # Private key of the wallet.
    RPC_URL: SolanaNetworks = SolanaNetworks.MAINNET_BETA
    USER_PERSONALITY: str = "I am a student who is interested in crypto and blockchain technology. I am a beginner and I am looking for a project to invest in. I want to make quick cash"

    # Backend Configuration
    TWEET_SCRAPE_SERVICE_URL: str # URL of my own personal tweet scrape service

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
