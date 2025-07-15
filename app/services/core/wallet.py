import typing as t
from abc import ABC, abstractmethod


class BaseWalletService(ABC):
    """
    Abstract base class for all wallet services
    """

    @abstractmethod
    def get_balance(self, token_address: t.Optional[str] = None) -> t.Optional[float]:
        """
        Get the balance of the wallet for a given token.
        
        Args:
            token_address: The token address. If None, returns SOL balance.
        
        Returns:
            Token balance (in token units for tokens, SOL units for SOL)
        """
        pass

    @abstractmethod
    def swap_token(self, from_token_address: str, to_token_address: str, amount: float) -> t.Optional[float]:
        """
        Swap a token.
        
        Args:
            from_token_address: Source token address ("SOL" for SOL)
            to_token_address: Target token address ("SOL" for SOL)
            amount: Amount to swap (in token units)
        
        Returns:
            Amount received from the swap (in token units)
        """
        pass
        
