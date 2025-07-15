import typing as t

from aiogram.types import URLInputFile  

from app.core.logging import logger
from app.services.core.notification import BaseNotificationService
from app.providers.bot_controller import get_bot_controller
from app.providers.bot import get_bot
from app.utils.action_buttons import get_action_buttons


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

    async def send_notification(self, message: str, token_address: str, is_buy_action: bool = True, amount: t.Optional[float] = None) -> None:
        """Send a notification message to the user.

        Args:
            message (str): The message to send, supports Markdown formatting
        """
        await self._bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=get_action_buttons(token_address, is_buy_action=is_buy_action, amount=amount)
        )
        logger.info(f"Sent notification to {self.chat_id}: {message}")

    async def send_image(self, image_url: str, message: str, token_address: str, is_buy_action: bool = True, amount: t.Optional[float] = None) -> None:
        await self._bot.send_photo(
            chat_id=self.chat_id,
            photo=URLInputFile(image_url),
            caption=message,
            parse_mode="Markdown",
            reply_markup=get_action_buttons(token_address, is_buy_action=is_buy_action, amount=amount)
        )
        logger.info(f"Sent image to {self.chat_id}: {message}")


if __name__ == "__main__":
    import asyncio
    
    async def main():
        notification_service = TelegramNotificationService(chat_id=1234567890)
        await notification_service.send_notification("Hello world! *bold* _italic_ [link](https://www.google.com)")
        print("Notification sent!")

    asyncio.run(main())


