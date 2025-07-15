import typing as t

from tinydb import TinyDB, Query

from app.core.logging import logger
from app.core.config import config
from app.services.twitter.tweet import TweetFetcherService
from app.models.creators import TokenCreatorDetails

from app.repository.launchcoin import LaunchcoinCreatorRepository


launchcoin_creator_repository = LaunchcoinCreatorRepository()


async def create_launchcoin_background_job(username: str):
    """
    Background job for fetching tweets of believe launchcoin.
    """
    logger.info(f"Starting background job for {username}")
    
    try:
        # Initialize services
        tweet_fetcher = TweetFetcherService()
        token_creators: t.Optional[t.List[TokenCreatorDetails]] = tweet_fetcher.fetch_creator_details(username)

        result = []

        # check database for duplicates
        for tc in token_creators:
            if not launchcoin_creator_repository.is_token_creator_exists(tc):
                result.append(tc)
            else:
                logger.debug(f"Token creator already exists for {tc.token_address}")

        # Save token creators to database
        if result:
            launchcoin_creator_repository.save_token_creator_details(result)
            logger.info(f"Saved {len(result)} token creators to database")
            
        else:
            logger.info(f"No new token creators found for {username}")

    except Exception as e:
        logger.error(f"Error in launchcoin background job: {e}")
        raise e