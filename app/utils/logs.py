from aiogram import types

from app.core.logging import logger


def log_bot_incomming_message(message: types.Message):
    """Log incoming message from user"""
    logger.info(
        ">>> User[%s|%s:@%s]: %r",
        message.chat.id,
        message.from_user.id,
        message.from_user.username,
        message.text,
    )


def log_bot_outgoing_message(message: types.Message, answer: str):
    """Log outgoing message from bot"""
    logger.info(
        "<<< User[%s|%s:@%s]: %r",
        message.chat.id,
        message.from_user.id,
        message.from_user.username,
        answer,
    )