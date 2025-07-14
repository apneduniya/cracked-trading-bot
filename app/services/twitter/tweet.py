import typing as t
import re

from app.core.logging import logger
from app.services.core.api import APIService
from app.services.twitter.routes import TweetsFetcherRoutes
from app.models.tweets import Tweet
from app.models.creators import TokenCreatorDetails


class TweetFetcherService:
    def __init__(self):
        self.api = APIService[TweetsFetcherRoutes](
            service_name="tweets_fetcher",
            base_url=TweetsFetcherRoutes.BASE
        )

    def fetch_tweets(self, username: str) -> t.Optional[t.List[Tweet]]:
        """
        Fetch tweets from the Twitter API
        """
        response = self.api.get(TweetsFetcherRoutes.TWEETS, params={"username": username})
        if response:
            return [Tweet(**tweet) for tweet in response]
        return None

    def fetch_creator_details(self, username: str) -> t.Optional[t.List[TokenCreatorDetails]]:
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

                token_creators.append(
                    TokenCreatorDetails(
                        username=username,
                        token_address=token_address,
                        token_name=token_name,
                        token_symbol=token_symbol
                    )
                )


        return token_creators if token_creators else None
