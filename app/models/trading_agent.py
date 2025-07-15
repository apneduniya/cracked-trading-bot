import typing as t

from pydantic import BaseModel, Field, field_validator


class TradingAgentResponse(BaseModel):
    action: t.Literal["buy", "sell", "hold"] = Field(description="The action to take on the token. It can be 'buy', 'sell', or 'hold'.", default="hold")
    reason: str = Field(description="Tell about the reason for the action, briefly (like what the product founder did, what you think, etc.). It can be in markdown format.")
    confidence: int = Field(description="The confidence in the action. It is a number between 0 and 100.")
    capital_allocation: int = Field(description="The percentage of the available capital to allocate to the token. It is a number between 0 and 100.", default=0)

    @field_validator("action")
    def validate_action(cls, v: t.Literal["buy", "sell", "hold"]) -> t.Literal["buy", "sell", "hold"]:
        if v not in ["buy", "sell", "hold"]:
            raise ValueError("Action must be 'buy', 'sell', or 'hold'.")
        return v

    @field_validator("confidence")
    def validate_confidence(cls, v: int) -> int:
        if v < 0 or v > 100:
            raise ValueError("Confidence must be between 0 and 100.")
        return v


    @field_validator("capital_allocation")
    def validate_capital_allocation(cls, v: int) -> int:
        if v < 0 or v > 100:
            raise ValueError("Capital allocation must be between 0 and 100.")
        return v

    
