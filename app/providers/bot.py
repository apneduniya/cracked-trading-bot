"""Bot provider

This module provides a bot instance for the application which helps to not create a new instance of the bot in each module.
(As Telegram only allows a single bot instance to be running at any given time for a specific bot token)
"""

import typing as t

from app.core.logging import logger
from app.core.config import config
from aiogram import Bot


_bot: t.Optional[Bot] = None


def get_bot() -> Bot:
    """Lazy initialization of the bot instance using a singleton pattern.
    
    This function ensures only one bot instance exists throughout the application lifecycle.
    The bot is initialized only when first requested, following the lazy initialization pattern.
    
    Returns:
        Bot: The singleton bot instance
    """
    global _bot
    if _bot is None:
        logger.info("Initializing the Bot instance using the token.")
        _bot = Bot(token=config.BOT_TOKEN)
    else:
        logger.info("Bot instance already initialized. Returning the existing instance.")
    return _bot