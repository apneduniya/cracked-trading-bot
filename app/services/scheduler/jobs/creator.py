import typing as t

from app.core.config import config
from app.core.logging import logger
from app.models.tweets import Tweet
from app.services.twitter.tweet import TweetFetcherService

from app.repository.creator import CreatorRepository
from app.services.agents.trading import TradingAgent
from app.services.notification.telegram import TelegramNotificationService


creator_repository = CreatorRepository()


async def create_creator_background_job(usernames: t.List[str]):
    """
    Background job for fetching creator's posts.
    """
    logger.info(f"Starting background job for creator's posts analysis")
    notification_service: t.Optional[TelegramNotificationService] = None
    try:
        # Initialize services
        tweet_fetcher = TweetFetcherService()
        trading_agent = TradingAgent()
        notification_service = TelegramNotificationService(chat_id=config.TELEGRAM_CHAT_ID)
        await notification_service.initialize()

        for username in usernames:
            creator_posts: t.Optional[t.List[Tweet]] = tweet_fetcher.fetch_tweets(username)

            if not creator_posts:
                logger.debug(f"No creator posts found for {username}")
                continue

            result = [] # List of creator posts to save to database

            # check if creator posts already exist in database
            for cp in creator_posts:
                if not creator_repository.is_creator_posts_exists(cp.url):
                    # AI Analysis of the creator's post
                    logger.info(f"Analyzing creator post for {username} - {cp.url}")
                    try:
                        trading_agent_response = await trading_agent.response(username, [cp.description])
                        if trading_agent_response:
                            logger.info(f"Trading agent response: {trading_agent_response}")
                            # Send notification to the user
                            logger.info(f"Sending notification to the user for {username} - {cp.url}")
                            await notification_service.send_notification(f"Trading decision for {username}: {trading_agent_response.action}")
                        else:
                            logger.warning(f"Trading agent returned no response for {username} - {cp.url}")
                    except Exception as e:
                        logger.error(f"Error analyzing creator post for {username} - {cp.url}: {str(e)}")
                        continue

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
    
    finally:
        if notification_service:
            await notification_service.end()