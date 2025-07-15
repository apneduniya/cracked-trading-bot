import typing as t

from app.core.logging import logger
from app.models.creators import CreatorPosts
from app.models.tweets import Tweet
from app.services.twitter.tweet import TweetFetcherService

from app.repository.creator import CreatorRepository


creator_repository = CreatorRepository()


async def create_creator_background_job(usernames: t.List[str]):
    """
    Background job for fetching creator's posts.
    """
    logger.info(f"Starting background job for creator's posts analysis")
    
    try:
        # Initialize services
        tweet_fetcher = TweetFetcherService()

        for username in usernames:
            creator_posts: t.Optional[t.List[Tweet]] = tweet_fetcher.fetch_tweets(username)

            if not creator_posts:
                logger.debug(f"No creator posts found for {username}")
                continue

            result = []

            # check if creator posts already exist in database
            for cp in creator_posts:
                if not creator_repository.is_creator_posts_exists(cp):
                    result.append(cp)
                else:
                    logger.debug(f"Creator post already exists for {username}")

            # Save creator post's username and url to database
            if result:
                creator_repository.save_creator_posts(result)
                logger.info(f"Saved {len(result)} creator posts to database")
                
            else:
                logger.info(f"No new creator posts found for {username}")

    except Exception as e:
        logger.error(f"Error in creator background job: {e}")
        raise e