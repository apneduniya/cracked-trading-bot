"""
Common token addresses and network endpoints for Solana.
"""

from enum import Enum

class CommonTokens(Enum):
    """
    Common tokens for Solana.
    """
    USDC: str = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    USDT: str = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    USDS: str = "USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA"
    SOL: str = "So11111111111111111111111111111111111111112"
    jitoSOL: str = "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn"
    bSOL: str = "bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1"
    mSOL: str = "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"
    BONK: str = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"


class SolanaNetworks(Enum):
    """
    Common networks for Solana.
    """
    MAINNET_BETA: str = "https://api.mainnet-beta.solana.com"
    DEVNET: str = "https://api.devnet.solana.com"
    TESTNET: str = "https://api.testnet.solana.com"

