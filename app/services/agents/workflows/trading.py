import typing as t

from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.workflow import Workflow

from app.core.config import config
from app.core.logging import logger
from app.models.trading_agent import TradingAgentResponse
from app.repository.launchcoin import LaunchcoinCreatorRepository
from app.static.prompts.trading_agent import SYSTEM_PROMPT, AUTONOMOUS_ACCESS_PROMPT, PROMPT
from app.services.data.token_data import TokenDataService


class TradingWorkflow(Workflow):
    system_prompt = SYSTEM_PROMPT.format(
        trading_agent_type=config.TRADING_AGENT_TYPE,
        user_personality=config.USER_PERSONALITY,
        post_system_prompt=AUTONOMOUS_ACCESS_PROMPT if config.AUTONOMOUS_TRADING else ""
    )

    agent = Agent(
        model=OpenAIChat(
            id=config.TRADING_AGENT_MODEL,
            api_key=config.OPENAI_API_KEY
        ),
        instructions=system_prompt,
        response_model=TradingAgentResponse,
        markdown=True,
        add_datetime_to_instructions=True,
    )

    async def arun(self, username: str, founder_tweets: t.List[str], user_wallet_balance: float, user_token_hold: float) -> t.AsyncIterator[RunResponse]:
        self.launchcoin_creator_repository = LaunchcoinCreatorRepository()

        logger.info(f"Getting token creator details for username: {username}")
        token_creator_details = self.launchcoin_creator_repository.get_token_details_by_username(username)
        if not token_creator_details:
            logger.info(f"Token creator details not found for username: {username}")
            # In async generators, use return without a value to end the generator
            return

        token_data_service = TokenDataService(token_address=token_creator_details.token_address)
        token_data = token_data_service.search_token_details()
        if not token_data:
            logger.info(f"Token data not found for token address: {token_creator_details.token_address}")
            # In async generators, use return without a value to end the generator
            return

        prompt = PROMPT.format(
            token_name=f"{token_creator_details.token_name} ({token_creator_details.token_symbol})",
            token_details=token_data.model_dump_json(),
            founder_tweets="\n".join(founder_tweets),
            token_hold=user_token_hold,
            wallet_balance=user_wallet_balance
        )

        try:
            agent_response = await self.agent.arun(prompt=prompt)
            if agent_response.content:
                yield RunResponse(
                    content=agent_response.content,
                )
            else:
                logger.info("No response from trading agent")
        except Exception as e:
            logger.error(f"Error in trading workflow: {e}")
            # In async generators, use return without a value to end the generator
            return
