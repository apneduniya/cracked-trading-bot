import typing as t
import base64
import json

from solders.pubkey import Pubkey # type: ignore
from solders.rpc.errors import InvalidParamsMessage # type: ignore
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair # type: ignore
from spl.token.instructions import get_associated_token_address

from jupiter_python_sdk.jupiter import Jupiter
from solders.transaction import VersionedTransaction # type: ignore
from solders.message import to_bytes_versioned # type: ignore
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Processed

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
        
        self.solana_client = AsyncClient(config.RPC_URL.value)
        logger.debug("WalletService initialized")

    async def get_balance(self, token_address: t.Optional[str] = None) -> float:
        try:
            if token_address is None:
                token_address = CommonTokens.SOL.value

            logger.debug(f"Getting balance for token: {token_address}")

            user_public_key: Pubkey = await self.__get_public_key()
            token_mint: Pubkey = Pubkey.from_string(token_address)

            # Get the associated token address (ATA)
            ata = get_associated_token_address(owner=user_public_key, mint=token_mint)
            print(f"ATA: {ata}")
            
            balance = await self.solana_client.get_token_account_balance(ata)
            logger.debug(f"Successfully got balance: {balance}")

            return balance    
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0.0
    
    async def _get_balance_fallback(self, token_address: str) -> float:
        """
        Fallback method to get balance when the main method fails
        """
        try:
            # For SPL tokens, if the account doesn't exist, the balance is 0
            # This is a common scenario when you don't hold the token
            logger.debug(f"Token account doesn't exist for {token_address}, returning 0.0")
            return 0.0
        except Exception as e:
            logger.error(f"Error in fallback balance method: {e}")
            return 0.0
    
    async def swap_token(self, from_token_address: str, to_token_address: str, amount: float) -> t.Optional[str]:
        try:
            logger.info(f"Attempting to swap {amount} from {from_token_address} to {to_token_address} on Jupiter...")

            # Prepare keypair and Jupiter client
            keypair = Keypair.from_base58_string(self.private_key)
            async_client = self.solana_client
            jupiter = Jupiter(
                async_client=async_client,
                keypair=keypair,
                # Updated to use latest Jupiter API endpoints (lite-api.jup.ag for free usage)
                quote_api_url="https://lite-api.jup.ag/swap/v1/quote?",
                swap_api_url="https://lite-api.jup.ag/swap/v1/swap"
            )

            # Jupiter expects amount in smallest units (e.g. lamports for SOL, decimals for SPL)
            # We'll assume amount is already in smallest units (caller responsibility)
            transaction_data = await jupiter.swap(
                input_mint=from_token_address,
                output_mint=to_token_address,
                amount=int(amount),
                slippage_bps=50,  # 0.5% slippage
            )
            if not transaction_data:
                logger.error("No transaction data returned from Jupiter swap API.")
                return None

            # Decode and sign transaction
            raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(transaction_data))
            signature = keypair.sign_message(to_bytes_versioned(raw_transaction.message))
            signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
            opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
            result = await async_client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
            transaction_id = json.loads(result.to_json())['result']
            logger.info(f"Swap successful! Transaction Signature: {DEFAULT_BLOCK_EXPLORER_URL}{transaction_id}")
            return transaction_id

        except Exception as e:
            logger.error(f"Error: Swap failed: {e}")
            return None
        
    async def get_wallet_address(self) -> str:
        """
        Get the wallet's public address
        """
        public_key = await self.__get_public_key()
        return str(public_key)
    
    async def __get_public_key(self) -> Pubkey:
        keypair = Keypair.from_base58_string(self.private_key)
        return keypair.pubkey()
        

if __name__ == "__main__":
    import asyncio
    import requests

    async def main():
        wallet_service = WalletService()
        
        sol_mint = CommonTokens.SOL.value
        usdc_mint = CommonTokens.USDC.value

        # 1. Get SOL price in USDC from Jupiter price API V3 (V4 is deprecated)
        # Use the correct V3 endpoint format
        price_url = f"https://lite-api.jup.ag/price/v3/price?ids={sol_mint}"
        try:
            price_resp = requests.get(price_url)
            price_resp.raise_for_status()
            price_data = price_resp.json()
            
            # V3 API has different response format
            if 'data' in price_data and sol_mint in price_data['data']:
                sol_price = float(price_data['data'][sol_mint]['price'])
            else:
                # Fallback: assume 1 SOL = 200 USDC if API fails
                print("Warning: Could not fetch SOL price, using fallback price")
                sol_price = 200.0
        except Exception as e:
            print(f"Error fetching price: {e}, using fallback price")
            sol_price = 200.0  # Fallback price

        # 2. Calculate how much SOL to swap for 0.2 USDC
        usdc_to_swap = 0.2
        sol_to_swap = usdc_to_swap / sol_price

        # 3. Convert SOL to lamports (1 SOL = 1_000_000_000 lamports)
        lamports_to_swap = int(sol_to_swap * 1_000_000_000)

        print(f"SOL price: ${sol_price:.2f}")
        print(f"Swapping {lamports_to_swap} lamports ({sol_to_swap:.8f} SOL) for {usdc_to_swap} USDC...")

        # 4. Call swap_token
        tx_sig = await wallet_service.swap_token(
            from_token_address=sol_mint,
            to_token_address=usdc_mint,
            amount=lamports_to_swap
        )
        print(f"Swap transaction signature: {tx_sig}")

    asyncio.run(main())


