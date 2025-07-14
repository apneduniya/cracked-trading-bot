


from pydantic import BaseModel


class TokenCreatoDetails(BaseModel):
    username: str
    token_address: str
    token_name: str
    token_symbol: str


