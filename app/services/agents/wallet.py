import typing as t

from solders.pubkey import Pubkey # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
from agentipy.tools.trade import TradeManager

from app.core.config import config
from app.core.logging import logger
from app.services.core.wallet import BaseWalletService
from app.static.tokens import CommonTokens
from app.static.default import DEFAULT_BLOCK_EXPLORER_URL


class WalletService(BaseWalletService):
    """
    Service for managing the solana wallet.
    """

    def __init__(self):
        self.private_key: t.Optional[str] = config.PRIVATE_KEY or None
        
        if not self.private_key:
            logger.warning("No private key provided for wallet")
            raise ValueError("Private key is required for wallet operations")
        
        self.agentipy_client = SolanaAgentKit(
            private_key=self.private_key,
            rpc_url=config.RPC_URL.value,
        )
        
        logger.debug("WalletService initialized")

    async def get_balance(self, token_address: t.Optional[str] = None) -> t.Optional[float]:
        try:
            if token_address is None:
                token_address = CommonTokens.SOL.value

            return await BalanceFetcher.get_balance(self.agentipy_client, token_address)
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None
    
    async def swap_token(self, from_token_address: str, to_token_address: str, amount: float) -> t.Optional[str]:
        try:
            logger.info(f"Attempting to swap {amount} from {from_token_address} to {to_token_address} on Jupiter...")

            # Prepare mints
            input_mint = Pubkey.from_string(from_token_address)
            output_mint = Pubkey.from_string(to_token_address)

            transaction_signature = await TradeManager.trade(
                agent=self.agentipy_client,
                output_mint=output_mint,
                input_amount=amount,
                input_mint=input_mint
            )

            logger.info("Swap successful!")
            logger.info(f"Transaction Signature: {DEFAULT_BLOCK_EXPLORER_URL}{transaction_signature}")

            return transaction_signature

        except Exception as e:
            logger.error(f"Error: Swap failed: {e}")
            return None


