from aiogram import types

from app.bot_controller.router import Router
from app.core.config import config
from app.core.logging import logger


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


@base_router.callback_query(lambda callback: callback.data.startswith("buy_"))
async def handle_buy_callback(callback_query: types.CallbackQuery):
    """
    Handle the buy button callback query.
    
    Args:
        callback_query: The callback query from the buy button
    """
    try:
        # Extract token address from callback data
        # Format: "buy_{token_address}_{amount}"
        token_address = callback_query.data.split("_")[1] # {token_address}
        amount = callback_query.data.split("_")[2] # {amount}
        
        logger.info(f"Buy callback received for token: {token_address}")
        
        # Answer the callback query to remove the loading state
        await callback_query.answer()
        
        # Implement buy logic here
        # For now, just send a confirmation message
        await callback_query.message.answer(
            f"🔄 Processing buy request for token: `{token_address}`\n\n"
            f"This feature is under development. The trading agent will handle the buy operation.\n\n"
            f"Amount: `{amount}`",
            parse_mode="Markdown"
        )
        
        # TODO: Implement actual buy logic here
        # This could involve:
        # 1. Validating the token address
        # 2. Checking user balance
        # 3. Executing the buy transaction
        # 4. Sending confirmation/failure message
        
        logger.info(f"Buy callback processed successfully for token: {token_address}")
        
    except Exception as e:
        logger.error(f"Error processing buy callback: {e}")
        await callback_query.answer("❌ Error processing buy request", show_alert=True)


# @base_router.register()
# async def common(message: types.Message):
#     print("\ncommon\n")




