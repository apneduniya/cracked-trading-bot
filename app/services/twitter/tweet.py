import typing as t
import re

from tinydb import TinyDB, Query

from app.core.logging import logger
from app.services.core.api import APIService
from app.services.twitter.routes import TweetsFetcherRoutes
from app.models.tweets import Tweet
from app.models.token_creators import TokenCreatoDetails
from app.static.default import CREATORS_DATABASE_FILE


class TweetFetcherService:
    def __init__(self):
        self.api = APIService[TweetsFetcherRoutes](
            service_name="tweets_fetcher",
            base_url=TweetsFetcherRoutes.BASE
        )
        self.db = TinyDB(CREATORS_DATABASE_FILE)

    def fetch_tweets(self, username: str) -> t.Optional[t.List[Tweet]]:
        """
        Fetch tweets from the Twitter API
        """
        response = self.api.get(TweetsFetcherRoutes.TWEETS, params={"username": username})
        if response:
            return [Tweet(**tweet) for tweet in response]
        return None

    def fetch_creator_details(self, username: str) -> t.Optional[t.List[TokenCreatoDetails]]:
        """
        Fetch creator details from the Twitter API
        """
        recent_tweets = self.fetch_tweets(username)
        if not recent_tweets:
            return None
        
        token_creators = []
        for tweet in recent_tweets:
            tweet_description = tweet.description

            # Regex to extract creator username, token name, token symbol, and token address from the tweet description
            pattern = r"@launchcoin\s+@(\w+)\s+Your coin '([^']+)' \(([^)]+)\) is live! Link: https://believe\.app/coin/([A-Za-z0-9]+)"
            match = re.search(pattern, tweet_description)

            if match:
                username = match.group(1)
                token_name = match.group(2)
                token_symbol = match.group(3)
                token_address = match.group(4)

                # check database for duplicates
                existing_token_creators = self.db.search(Query().token_address == token_address)
                if not existing_token_creators:
                    logger.info(f"Token: {token_address} adding to database")

                    token_creators.append(
                        TokenCreatoDetails(
                            username=username,
                            token_address=token_address,
                            token_name=token_name,
                            token_symbol=token_symbol
                        )
                    )
                else:
                    logger.debug(f"Token: {token_address} already exists in database")


        return token_creators if token_creators else None
