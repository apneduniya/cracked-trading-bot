import typing as t
from tinydb import TinyDB, Query

from app.models.creators import TokenCreatorDetails
from app.static.default import CREATORS_DATABASE_FILE


class LaunchcoinCreatorRepository:
    """
    Repository for believe (launchcoin) creator details.
    """
    def __init__(self):
        self.db = TinyDB(CREATORS_DATABASE_FILE)

    def get_token_creator_details(self, username: str) -> t.Optional[TokenCreatorDetails]:
        return TokenCreatorDetails(**self.db.search(Query().username == username)[0]) if self.db.search(Query().username == username) else None
    
    def save_token_creator_details(self, token_creator_details: TokenCreatorDetails) -> None:
        self.db.insert(token_creator_details.model_dump())

    def is_token_creator_exists(self, token_creator_details: TokenCreatorDetails) -> bool:
        return self.db.search(Query().token_address == token_creator_details.token_address) is not None


