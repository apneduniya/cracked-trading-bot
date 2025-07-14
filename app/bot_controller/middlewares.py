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
        message: types.Message = event.message

        log_bot_incomming_message(message)
        result = await handler(event, data)

        log_bot_outgoing_message(message, result)

        return result
        

