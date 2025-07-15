import typing as t
import json

from app.core.logging import logger

from app.services.core.notification import BaseNotificationService
from app.services.core.api import APIService
from app.services.notification.routes import TelegramAPIRoutes

from app.providers.bot_controller import get_bot_controller
from app.providers.bot import get_bot


class TelegramNotificationService(BaseNotificationService):
    """Telegram notification service for sending messages to users via Telegram.

    This service handles sending notifications to specific Telegram users by their chat ID.
    It manages the bot controller lifecycle and provides methods for sending formatted messages.

    Attributes:
        chat_id (int): The chat ID to send notifications to
    """

    def __init__(self, chat_id: int):
        """Initialize the Telegram notification service.

        Args:
            chat_id (int): The chat ID to send notifications to
        """
        self._bot_controller = get_bot_controller()
        self._bot = get_bot()
        
        self.chat_id: int = chat_id
        self.telegram_api: APIService[TelegramAPIRoutes] = None

    async def initialize(self) -> None:
        """Initialize the service by getting the chat ID for the chat ID.

        This method:
        1. Temporarily stops the bot controller to prevent message conflicts
        2. Attempts to find the chat ID for the given chat ID
        3. Raises an error if the chat ID cannot be found

        Raises:
            ValueError: If the chat ID cannot be found for the given chat ID
        """
        await self._bot_controller.close()

        self.telegram_api = APIService[TelegramAPIRoutes](
            service_name="telegram",
            base_url=TelegramAPIRoutes.BASE
        )

    async def send_notification(self, message: str) -> None:
        """Send a notification message to the user.

        Args:
            message (str): The message to send, supports Markdown formatting
        """
        await self._bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown"
        )
        logger.info(f"Sent notification to {self.chat_id}: {message}")

    async def _get_updates(self) -> t.List[t.Any]:
        """Get updates from the Telegram bot.

        Returns:
            List[t.Any]: A list of updates from the bot
        """
        return self.telegram_api.get(TelegramAPIRoutes.GET_UPDATES)
    
    async def end(self) -> None:
        """End the service by restarting the bot controller.

        This method restarts the bot controller to resume normal bot operation
        after sending notifications.
        """
        await self._bot_controller.start()


if __name__ == "__main__":
    import asyncio
    
    async def main():
        notification_service = TelegramNotificationService(chat_id=1234567890)
        await notification_service.initialize()  # Initialize before use
        await notification_service.send_notification("Hello world! *bold* _italic_ [link](https://www.google.com)")
        print("Notification sent!")

    asyncio.run(main())


