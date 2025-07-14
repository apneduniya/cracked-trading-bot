


from pydantic import BaseModel


class TokenCreatorDetails(BaseModel):
    username: str
    token_address: str
    token_name: str
    token_symbol: str


class CreatorPosts(BaseModel):
    username: str
    url: str
