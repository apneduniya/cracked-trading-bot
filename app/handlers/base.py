from aiogram import types
import typing as t

from app.bot_controller.router import Router
from app.core.config import config
from app.core.logging import logger
from app.services.data.token_data import TokenDataService
from app.services.agents.wallet import WalletService
from app.static.default import DEFAULT_BLOCK_EXPLORER_URL
from app.static.tokens import CommonTokens


base_router = Router(name=__name__)
wallet_service = WalletService()


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
        token_symbol = TokenDataService(token_address).get_token_symbol()

        # Check if the user has enough balance in their wallet
        users_current_wallet_balance: float = await wallet_service.get_balance(CommonTokens.USDC.value)
        if users_current_wallet_balance == 0:
            logger.warning(f"User's current wallet balance is not found")
            return
        if users_current_wallet_balance < amount:
            logger.warning(f"User's current wallet balance is not enough to buy the token")
            return
                        
        # Answer the callback query to remove the loading state
        await callback_query.answer()
        
        logger.info(f"Buy callback received for {token_symbol} token of ${amount} with ${users_current_wallet_balance} in wallet")
        await callback_query.message.answer(
            f"🔄 Processing buy request for {token_symbol} token of ${amount}\n\n",
            parse_mode="Markdown"
        )

        transaction_signature = await wallet_service.swap_token(
            from_token_address=CommonTokens.USDC.value,
            to_token_address=token_address,
            amount=amount,
        )

        if transaction_signature is None:
            logger.error(f"Failed to swap token for {token_symbol} token of ${amount}")
            return
        
        logger.info(f"Buy callback processed successfully for {token_symbol} token of ${amount}")
        await callback_query.message.answer(
            f"✅ Buy request for {token_symbol} token of ${amount} processed successfully\n\n"
            f"Transaction signature: {DEFAULT_BLOCK_EXPLORER_URL}{transaction_signature}",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error processing buy callback: {e}")
        await callback_query.answer("❌ Error processing buy request", show_alert=True)


@base_router.callback_query(lambda callback: callback.data.startswith("sell_"))
async def handle_sell_callback(callback_query: types.CallbackQuery):
    """
    Handle the sell button callback query.
    """
    try:
        # Extract token address from callback data
        # Format: "sell_{token_address}_{amount}"
        token_address = callback_query.data.split("_")[1] # {token_address}
        amount = callback_query.data.split("_")[2] # {amount}
        token_symbol = TokenDataService(token_address).get_token_symbol()

        users_current_wallet_balance: float = await wallet_service.get_balance(CommonTokens.USDC.value)
        if users_current_wallet_balance == 0:
            logger.warning(f"User's current wallet balance is 0")
            return
        
        # Answer the callback query to remove the loading state
        await callback_query.answer()
        
        logger.info(f"Sell callback received for {token_symbol} token of ${amount} with ${users_current_wallet_balance} in wallet")
        await callback_query.message.answer(
            f"🔄 Processing sell request for {token_symbol} token of ${amount}\n\n",
            parse_mode="Markdown"
        )

        transaction_signature = await wallet_service.swap_token(
            from_token_address=token_address,
            to_token_address=CommonTokens.USDC.value,
            amount=amount,
        )
        
        if transaction_signature is None:
            logger.error(f"Failed to swap token for {token_symbol} token of ${amount}")
            return
        
        logger.info(f"Sell callback processed successfully for {token_symbol} token of ${amount}")
        await callback_query.message.answer(
            f"✅ Sell request for {token_symbol} token of ${amount} processed successfully\n\n"
            f"Transaction signature: {DEFAULT_BLOCK_EXPLORER_URL}{transaction_signature}",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error processing sell callback: {e}")
        await callback_query.answer("❌ Error processing sell request", show_alert=True)


