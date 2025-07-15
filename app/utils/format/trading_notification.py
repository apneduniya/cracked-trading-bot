
from app.models.creators import TokenCreatorDetails
from app.models.tweets import Tweet
from app.models.trading_agent import TradingAgentResponse


def format_trading_notification(
    username: str,
    token_creator_details: TokenCreatorDetails,
    creator_post: Tweet,
    trading_agent_response: TradingAgentResponse
) -> str:
    """
    Format a comprehensive trading notification message for Telegram.
    
    Args:
        username: Creator's username
        token_creator_details: Token information
        creator_post: Tweet/post information
        trading_agent_response: AI trading analysis with confidence and capital allocation
    
    Returns:
        Formatted notification message string
    """
    # Action emojis and titles for visual indicators
    action_config = {
        "buy": {"emoji": "🟢", "title": "BUY SIGNAL"},
        "sell": {"emoji": "🔴", "title": "SELL SIGNAL"}, 
        "hold": {"emoji": "🟡", "title": "HOLD"}
    }
    
    config = action_config.get(trading_agent_response.action, {"emoji": "⚪", "title": "UNKNOWN"})
    
    # Start building the message
    lines = [
        f"{config['emoji']} **{config['title']}** {config['emoji']}",
        "",
        f"👤 **Creator**: [{username}](https://x.com/{username})",
        f"🪙 **Token**: {token_creator_details.token_name} (${token_creator_details.token_symbol})",
        f"📊 **Contract**: `{token_creator_details.token_address}`",
        "",
        f"📝 **Post**: {creator_post.title if creator_post.title else 'New Post'}",
        f"🔗 **Link**: {creator_post.url}",
        "",
        f"📈 **Confidence**: {trading_agent_response.confidence}%"
    ]
    
    # Add capital allocation only for buy/sell actions
    if trading_agent_response.action in ["buy", "sell"] and trading_agent_response.capital_allocation > 0:
        lines.append(f"💰 **Capital Allocation**: {trading_agent_response.capital_allocation}%")
    
    # Add analysis
    lines.extend([
        "",
        f"💡 **Analysis**:\n{trading_agent_response.reason}",
        "",
        # f"📄 **Post Content**: {creator_post.description[:200]}{'...' if len(creator_post.description) > 200 else ''}"
    ])
    
    return "\n".join(lines)
