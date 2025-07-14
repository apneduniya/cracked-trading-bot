import typing as t

from tinydb import TinyDB, Query

from app.core.logging import logger
from app.core.config import config
from app.models.creators import CreatorPosts
from app.models.tweets import Tweet
from app.services.twitter.tweet import TweetFetcherService

from app.static.default import CREATORS_TWEETS_DATABASE_FILE


db = TinyDB(CREATORS_TWEETS_DATABASE_FILE)


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
                existing_creator_posts = db.search(Query().url == cp.url)
                if not existing_creator_posts:
                    result.append(cp)
                else:
                    logger.debug(f"Creator post already exists for {username}")

            # Save creator post's username and url to database
            if result:
                db.insert_multiple([CreatorPosts(username=username, url=cp.url).model_dump() for cp in result])
                logger.info(f"Saved {len(result)} creator posts to database")
                
            else:
                logger.info(f"No new creator posts found for {username}")

    except Exception as e:
        logger.error(f"Error in creator background job: {e}")
        raise e