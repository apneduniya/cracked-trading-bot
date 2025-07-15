import typing as t
import asyncio

from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat

from app.core.config import config
from app.core.logging import logger
from app.models.trading_agent import TradingAgentResponse
from app.static.prompts.trading_agent import SYSTEM_PROMPT, PROMPT, AUTONOMOUS_ACCESS_PROMPT
from app.services.data.token_data import TokenDataService
from app.repository.launchcoin import LaunchcoinCreatorRepository


class TradingAgent:
    """
    Trading agent that makes decisions on whether to buy/sell/hold a token based on the founder's tweets.
    """
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT.format(
            trading_agent_type=config.TRADING_AGENT_TYPE, 
            post_system_prompt=AUTONOMOUS_ACCESS_PROMPT if config.AUTONOMOUS_TRADING else ""
        )
        self.launchcoin_creator_repository = LaunchcoinCreatorRepository()


    async def response(self, username: str, founder_tweets: t.List[str]) -> t.Optional[TradingAgentResponse]:
        logger.info(f"Getting token creator details for username: {username}")
        token_creator_details = self.launchcoin_creator_repository.get_token_details_by_username(username)
        if not token_creator_details:
            logger.info(f"Token creator details not found for username: {username}")
            return None
        
        token_data_service = TokenDataService(token_address=token_creator_details.token_address)
        token_data = token_data_service.search_token_details()
        if not token_data:
            logger.info(f"Token data not found for token address: {token_creator_details.token_address}")
            return None

        logger.info(f"Getting trading agent response for username: {username}")
        
        # Validate OpenAI API key
        if not config.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is not set in environment variables")
            return None
        
        try:
            agent = Agent(
                model=OpenAIChat(id=config.TRADING_AGENT_MODEL, api_key=config.OPENAI_API_KEY),
                instructions=self.system_prompt,
                response_model=TradingAgentResponse,
                markdown=True,
            )
            prompt = PROMPT.format(
                token_name=f"{token_creator_details.token_name} ({token_creator_details.token_symbol})",
                token_details=token_data.model_dump_json(),
                founder_tweets="\n".join(founder_tweets)
            )
            
            logger.info(f"Sending request to OpenAI API for trading decision...")
            response: RunResponse = await asyncio.wait_for(
                agent.arun(prompt=prompt),
                timeout=60.0  # 60 second timeout
            )
            logger.info(f"Received response from OpenAI API: {response}")
            return response.content
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout error: OpenAI API call timed out after 60 seconds for username: {username}")
            return None
        except Exception as e:
            logger.error(f"Error getting trading agent response for username {username}: {str(e)}")
            return None



