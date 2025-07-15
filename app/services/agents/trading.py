import typing as t

from app.core.logging import logger
from app.models.trading_agent import TradingAgentResponse
from app.services.agents.workflows.trading import TradingWorkflow


class TradingAgent:
    """
    Trading agent that makes decisions on whether to buy/sell/hold a token based on the founder's tweets.
    """
    def __init__(self):
        self.trading_workflow = TradingWorkflow()

    async def response(self, username: str, founder_tweets: t.List[str]) -> t.Optional[TradingAgentResponse]:
        try:
            logger.info(f"Running trading workflow for username: {username}")
            
            # Collect all responses from the workflow
            responses = []
            async for response in self.trading_workflow.arun(username, founder_tweets):
                responses.append(response)
            
            if not responses:
                logger.info("No response from trading workflow")
                return None
            
            # Get the last response content
            last_response = responses[-1]
            if not last_response.content:
                logger.info("No content in trading workflow response")
                return None
                
            # The content should already be a TradingAgentResponse object from the workflow
            if isinstance(last_response.content, TradingAgentResponse):
                logger.info(f"Trading agent response: {last_response.content}")
                return last_response.content
            else:
                logger.warning(f"Unexpected response type: {type(last_response.content)}")
                return None

        except Exception as e:
            logger.error(f"Error in trading agent: {e}")
            return None
