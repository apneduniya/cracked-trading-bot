from enum import Enum

from app.core.config import config


class TweetsFetcherRoutes(Enum):
    """
    Enum for tweets fetcher API routes
    """

    BASE = config.TWEET_SCRAPE_SERVICE_URL

    TWEETS = "/tweets"



