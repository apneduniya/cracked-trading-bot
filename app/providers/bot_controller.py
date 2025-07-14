"""Bot controller provider

This module provides a bot controller instance for the application which helps to not create a new instance of the bot controller in each module.
(As Telegram only allows a single bot instance to be running at any given time for a specific bot token)
"""

import typing as t

from app.core.logging import logger
from app.core.config import config

from app.bot_controller.bot_controller import BotController


_bot_controller: t.Optional[BotController] = None


def get_bot_controller() -> BotController:
    """Lazy initialization of the bot controller instance using a singleton pattern.
    
    This function ensures only one bot controller instance exists throughout the application lifecycle.
    The bot controller is initialized only when first requested, following the lazy initialization pattern.
    
    Returns:
        BotController: The singleton bot controller instance
    """
    global _bot_controller
    if _bot_controller is None:
        logger.info("Initializing the BotController instance, first time.")
        _bot_controller = BotController()
    else:
        logger.info("BotController instance already initialized. Returning the existing instance.")
    return _bot_controller