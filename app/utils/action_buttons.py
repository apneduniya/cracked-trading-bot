import typing as t

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.static.default import BUY_CALLBACK_DATA
from app.core.config import config


def get_action_buttons(token_address: str, is_buy_action: bool = True, amount: t.Optional[float] = None) -> InlineKeyboardMarkup:
    """
    Get the action buttons for the token.

    Args:
        token_address (str): The address of the token.

    Returns:
        InlineKeyboardMarkup: The action buttons for the token.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                *(
                    [
                        InlineKeyboardButton(
                            text="Buy",
                            callback_data=BUY_CALLBACK_DATA.format(token_address=token_address, amount=amount),
                        )
                    ] if not config.AUTONOMOUS_TRADING and is_buy_action else []
                ),
                InlineKeyboardButton(
                    text="View on Believe",
                    url=f"https://believe.app/coin/{token_address}"
                )
            ],
        ]
    )
