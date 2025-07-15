"""
Common token addresses and network endpoints for Solana.
"""

from enum import Enum

class CommonTokens(Enum):
    """
    Common tokens for Solana.
    """
    USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    USDT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    USDS = "USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA"
    SOL = "So11111111111111111111111111111111111111112"
    JITOSOL = "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn"
    BSOL = "bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1"
    MSOL = "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"
    BONK = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"


class SolanaNetworks(Enum):
    """
    Common networks for Solana.
    """
    MAINNET_BETA = "https://api.mainnet-beta.solana.com"
    DEVNET = "https://api.devnet.solana.com"
    TESTNET = "https://api.testnet.solana.com"

