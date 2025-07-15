import typing as t

from app.services.core.api import APIService
from app.services.data.route import TokenDataRoutes
from app.models.data.token_data import TokenData as TokenDataModel


class TokenDataService:
    """
    Service to get token data from the Jup API
    """

    def __init__(self, token_address: str):
        self.token_address = token_address
        self.api_service = APIService[TokenDataRoutes](
            service_name="token_data",
            base_url=TokenDataRoutes.BASE
        )

    def search_token_details(self) -> t.Optional[TokenDataModel]:
        """
        Request a search by token's symbol, name or mint address

        Args:
            query (str): The token's symbol, name or mint address

        Returns:
            TokenDataModel: The token data
        """
        response = self.api_service.get(TokenDataRoutes.TOKEN_DETAILS, params={"query": self.token_address})
        if response:
            return TokenDataModel(**response[0])
        return None
    
    def get_token_price(self) -> t.Optional[float]:
        """
        Get the price of the token in USD
        """
        response = self.api_service.get(TokenDataRoutes.TOKEN_DETAILS, params={"query": self.token_address})
        if response:
            token_details = TokenDataModel(**response[0])
            return token_details.usdPrice
        return None
    
    def get_token_symbol(self) -> t.Optional[str]:
        """
        Get the symbol of the token
        """
        response = self.api_service.get(TokenDataRoutes.TOKEN_DETAILS, params={"query": self.token_address})
        if response:
            token_details = TokenDataModel(**response[0])
            return token_details.symbol
        return None


if __name__ == "__main__":
    import json

    # token_data_service = TokenDataService("aKHs9C1kzwfopRJ8Z8mStNWhv1fVyzynSdHUDP5kBLV")
    token_data_service = TokenDataService("4HDPjV98ZJpDnc7FuyF2tsMDxkKhyPGs5yzyrEgvyBLV")
    token_data = token_data_service.search_token_details()
    symbol = token_data_service.get_token_symbol()
    price = token_data_service.get_token_price()

    print(
        json.dumps(token_data.model_dump(), indent=4)
    )
    print("symbol: ", symbol)
    print("price in usd: ", price)





