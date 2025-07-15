import typing as t

from app.core.config import config
from app.core.logging import logger
from app.models.trading_agent import TradingAgentResponse
from app.models.tweets import Tweet
from app.models.data.token_data import TokenData
from app.services.agents.wallet import WalletService
from app.services.data.token_data import TokenDataService
from app.services.twitter.tweet import TweetFetcherService
from app.static.tokens import CommonTokens

from app.repository.launchcoin import LaunchcoinCreatorRepository
from app.models.creators import TokenCreatorDetails, CreatorPosts
from app.repository.creator import CreatorRepository
from app.services.agents.trading import TradingAgent
from app.services.notification.telegram import TelegramNotificationService
from app.utils.format.trade_chart import get_simple_chart_image
from app.utils.format.trading_notification import format_trading_notification


creator_repository = CreatorRepository()
launchcoin_creator_repository = LaunchcoinCreatorRepository()
wallet_service = WalletService()




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

        for username in usernames:
            creator_posts: t.Optional[t.List[Tweet]] = tweet_fetcher.fetch_tweets(username)
            token_creator_details: t.Optional[TokenCreatorDetails] = launchcoin_creator_repository.get_token_details_by_username(username)
            if not token_creator_details:
                logger.warning(f"No token creator details found for {username}")
                continue

            if not creator_posts:
                logger.debug(f"No creator posts found for {username}")
                continue

            result: t.Optional[t.List[Tweet]] = [] # List of creator posts to save to database

            # check if creator posts already exist in database
            for cp in creator_posts:
                if not creator_repository.is_creator_posts_exists(cp.url):
                    # AI Analysis of the creator's post
                    logger.info(f"Analyzing creator post for {username} - {cp.url}")
                    try:
                        trading_agent_response: t.Optional[TradingAgentResponse] = await trading_agent.response(username, [cp.description], await wallet_service.get_balance(CommonTokens.USDC.value), await wallet_service.get_balance(token_creator_details.token_address))
                        if trading_agent_response:
                            logger.info(f"Trading agent response: {trading_agent_response}")
                            
                            # Format and send notification message
                            notification_message = format_trading_notification(
                                username=username,
                                token_creator_details=token_creator_details,
                                creator_post=cp,
                                trading_agent_response=trading_agent_response
                            )

                            # Get token chart image
                            token_chart_url: t.Optional[str] = None

                            token_data_service = TokenDataService(token_address=token_creator_details.token_address)
                            token_data: t.Optional[TokenData] = token_data_service.search_token_details()
                            if token_data:
                                token_chart_url = get_simple_chart_image(token_data)

                            # Action buttons
                            is_buy_action: bool = trading_agent_response.action == "buy"
                            is_sell_action: bool = trading_agent_response.action == "sell"

                            # Calculate the amount to allocate to the token
                            users_current_wallet_balance: t.Optional[float] = await wallet_service.get_balance(CommonTokens.USDC.value)
                            if users_current_wallet_balance is None:
                                logger.warning(f"User's current wallet balance is not found")
                                continue

                            amount: float = users_current_wallet_balance * (trading_agent_response.capital_allocation / 100)

                            # Send notification
                            logger.info(f"Sending notification to the user for {username} - {cp.url}")
                            if token_chart_url:
                                await notification_service.send_image(token_chart_url, notification_message, token_creator_details.token_address, is_buy_action=is_buy_action, is_sell_action=is_sell_action, amount=amount)
                            else:
                                await notification_service.send_notification(notification_message, token_creator_details.token_address, is_buy_action=is_buy_action, is_sell_action=is_sell_action, amount=amount)
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
                creator_repository.save_creator_posts([CreatorPosts(username=username, url=cp.url) for cp in result])
                logger.info(f"Saved {len(result)} creator posts to database")
                
            else:
                logger.info(f"No new creator posts found for {username}")

    except Exception as e:
        logger.error(f"Error in creator background job: {e}")
        raise e