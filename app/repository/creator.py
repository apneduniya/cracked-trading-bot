import typing as t
from tinydb import TinyDB, Query

from app.static.default import CREATORS_TWEETS_DATABASE_FILE
from app.models.creators import CreatorPosts


class CreatorRepository:
    """
    Repository for token creator's posts (project founders) who launch their token on believe (via launchcoin).
    """
    def __init__(self):
        self.db = TinyDB(CREATORS_TWEETS_DATABASE_FILE)

    def get_creator_posts(self, username: str) -> t.Optional[t.List[CreatorPosts]]:
        return [CreatorPosts(**cp) for cp in self.db.search(Query().username == username)] if self.db.search(Query().username == username) else None

    def save_creator_posts(self, creator_posts: t.List[CreatorPosts]) -> None:
        self.db.insert_multiple([cp.model_dump() for cp in creator_posts])

    def is_creator_posts_exists(self, url: str) -> bool:
        return bool(self.db.search(Query().url == url))