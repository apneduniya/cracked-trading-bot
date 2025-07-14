from aiogram import types

from app.bot_controller.router import Router
from app.core.config import config


base_router = Router(name=__name__)


@base_router.register(
    command="start",
    description="Start the bot",
)
async def send_welcome(message: types.Message):
    username = message.from_user.username

    return [
        f"Hello {username}! I'm Cracked Trading Bot!\n{config.BOT_DESCRIPTION}",
        "You can use /help command to view all available commands."
    ]


@base_router.register(
    command="help",
    description="View all available commands",
)
async def help(message: types.Message):
    all_commands = Router.get_all_commands()
    if not all_commands:
        return "No commands available."
    return "Available commands:\n" + "\n".join(all_commands)


# @base_router.register()
# async def common(message: types.Message):
#     print("\ncommon\n")




