import typing as t

from tinydb import TinyDB

from app.core.logging import logger
from app.core.config import config
from app.services.twitter.tweet import TweetFetcherService
from app.models.token_creators import TokenCreatoDetails

from app.static.default import DATABASE_FILE


db = TinyDB(DATABASE_FILE)


async def create_launchcoin_background_job(username: str):
    """
    Background job for fetching tweets of believe launchcoin.
    """
    logger.info(f"Starting background job for {username}")
    
    try:
        # Initialize services
        tweet_fetcher = TweetFetcherService()
        token_creators: t.Optional[t.List[TokenCreatoDetails]] = tweet_fetcher.fetch_creator_details(username)

        logger.info(f"Completed background job for {username}")

        # Save token creators to database
        if token_creators:
            db.insert_multiple([tc.model_dump() for tc in token_creators])
            logger.info(f"Saved {len(token_creators)} token creators to database")
            
        else:
            logger.info(f"No token creators found for {username}")

    except Exception as e:
        logger.error(f"Error in launchcoin background job: {e}")
        raise e