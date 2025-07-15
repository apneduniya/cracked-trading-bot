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
    


if __name__ == "__main__":
    token_data_service = TokenDataService("aKHs9C1kzwfopRJ8Z8mStNWhv1fVyzynSdHUDP5kBLV")
    token_data = token_data_service.search_token_details()
    print(token_data)





