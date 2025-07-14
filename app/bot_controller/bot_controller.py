from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiohttp.web_runner import GracefulExit

from app.core.logging import logger
from app.bot_controller import middlewares
from app import handlers
from app.providers.bot import get_bot


class BotController:
    """Controller class for managing the Telegram bot.

    This class handles the initialization, configuration, and operation of the Telegram bot.
    It manages middlewares, routers, and provides methods for sending messages and controlling
    the bot's lifecycle.

    Attributes:
        MIDDLEWARES (list): List of middleware classes to be registered with the dispatcher
        ROUTERS (list): List of router instances to be included in the dispatcher
    """

    MIDDLEWARES = [
        middlewares.AutoAnswerMiddleware,
    ]

    ROUTERS = [
        handlers.base_router,
    ]

    def __init__(self):
        """Initialize the BotController.

        Sets up the bot instance, dispatcher, and registers middlewares and routers.
        """
        self._bot = get_bot()
        self._dispatcher = Dispatcher()

        self._register_middlewares()
        self._register_routers()

    async def start(self) -> None:
        """Start the bot and begin polling for updates.

        This method starts the bot's polling process and handles various shutdown scenarios.
        It catches and logs exceptions, including graceful shutdown signals.

        Raises:
            Exception: Any unexpected errors during bot operation
        """
        try:
            logger.info("Starting bot...")
            await self._dispatcher.start_polling(self._bot)
        except Exception as error:
            logger.exception("Unexpected error: %r", error, exc_info=error)
        except (GracefulExit, KeyboardInterrupt, CancelledError):
            logger.info("Bot graceful shutdown...")

    async def close(self) -> None:
        """Close the bot and stop polling for updates.

        This method stops the bot's polling process and handles graceful shutdown.
        """
        await self._dispatcher.stop_polling()


    async def send_message(self, user_external_id: int, answer: str, parse_mode: str = ParseMode.HTML) -> None:
        """Send a message to a specific user.

        Args:
            user_external_id (int): The Telegram user ID to send the message to
            answer (str): The message text to send
            parse_mode (str, optional): The parse mode for the message. Defaults to HTML.
        """
        await self._bot.send_message(user_external_id, answer, parse_mode=parse_mode)

    def _register_middlewares(self) -> None:
        """Register all configured middlewares with the dispatcher."""
        for middleware in self.MIDDLEWARES:
            self._dispatcher.update.outer_middleware.register(middleware())

    def _register_routers(self) -> None:
        """Register all configured routers with the dispatcher."""
        self._dispatcher.include_routers(*self.ROUTERS)

