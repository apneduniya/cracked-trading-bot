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
            Balance as a float in UI units, or None if the account doesn't exist.
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
            Transaction signature
        """
        pass
        
