import typing as t

from aiogram import BaseMiddleware
from aiogram import types

from app.utils.logs import log_bot_incomming_message, log_bot_outgoing_message


class AutoAnswerMiddleware(BaseMiddleware):
    """
    - This logs the incoming message and the outgoing message.
    - This send the response from the handlers to the user.
    """

    async def __call__(
        self,
        handler: t.Callable[[types.TelegramObject, t.Dict[str, t.Any]], t.Awaitable[t.Any]],
        event: types.TelegramObject,
        data: t.Dict[str, t.Any],
    ) -> t.Any:
        # Handle different types of updates
        message: t.Optional[types.Message] = None
        
        if hasattr(event, 'message') and event.message:
            # Regular message
            message = event.message
        elif hasattr(event, 'callback_query') and event.callback_query:
            # Callback query - get the message from the callback query
            message = event.callback_query.message
        elif isinstance(event, types.CallbackQuery):
            # Direct callback query event
            message = event.message
        
        # Only log if we have a valid message
        if message:
            log_bot_incomming_message(message)
        
        result = await handler(event, data)

        # Only log outgoing message if we have a valid message
        if message:
            log_bot_outgoing_message(message, result)

        return result
        

