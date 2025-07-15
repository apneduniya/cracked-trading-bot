<h1 align="center">Cracked Trading Bot 🤖</h1>

<p align="center">Believe X AI-powered personal crypto trading bot that runs 24/7 on Believe tokens, analyzing token creators' posts and making real-time buy/sell decisions - all reported via Telegram.</p>

## 🎥 DEMO
[![demo video](https://i.vimeocdn.com/video/placeholder-thumbnail.jpg)](https://www.veed.io/view/your-demo-video)

## 📙 Features
- **24/7 Autonomous Operation**: Continuously monitors token creators and market opportunities
- **AI-Powered Decision Making**: Uses GPT-4o to analyze founder posts and make trading decisions
- **Smart Capital Allocation**: Calculates optimal investment amounts with confidence scoring (0-100%)
- **Multi-Agent Personalities**: Choose from `chill`, `aggressive`, or `moderate` trading strategies
- **Believe.app Integration**: Monitors tokens launched via @launchcoin
- **Jupiter Swap Integration**: Executes trades through Jupiter's DEX aggregator
- **Real-time Tweet Monitoring**: Tracks founder posts every 5 minutes
- **Interactive Telegram Bot**: One-click buy/sell actions with rich notifications
- **Price Chart Integration**: Automated chart generation and embedding
- **Multi-Token Support**: SOL, USDC, USDT, and all SPL tokens
- **Autonomous & Manual Modes**: Toggle between fully automated trading or manual confirmation

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Solana wallet with private key
- Telegram bot token
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cracked-trading-bot.git
   cd cracked-trading-bot
   ```

2. **Run the setup script**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit with your credentials
   nano .env
   ```

4. **Required Environment Variables**
   ```env
   BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   OPENAI_API_KEY=your_openai_api_key
   PRIVATE_KEY=your_solana_wallet_private_key
   TWEET_SCRAPE_SERVICE_URL=your_tweet_scrape_service_url
   TRADING_AGENT_TYPE=chill  # or aggressive, moderate
   AUTONOMOUS_TRADING=false  # or true for fully automated
   ```

5. **Start the bot**
   ```bash
   source ~/.venvs/cracked-trading-bot/bin/activate
   python app/main.py
   ```

## ⚙️ Configuration

### Trading Agent Types
- **Chill**: Conservative approach with higher confidence thresholds
- **Aggressive**: High-risk, high-reward strategy with lower barriers
- **Moderate**: Balanced approach between risk and reward

### Scheduler Settings
- **Creator Monitoring**: Every 5 minutes (configurable)
- **Launchcoin Tracking**: Every 15 minutes (configurable)
- **Startup Behavior**: Configurable immediate execution

### Security Features
- **Private Key Protection**: Secure wallet integration with error handling
- **Rate Limiting**: API protection against abuse
- **Logging**: Comprehensive audit trail for all actions

## 🔧 Advanced Features

### Custom Tweet Scraping
I have built my own X scraper which doesn't require any API keys and can scrape upto 30 recent tweets. I have kept it as seperate service so you need to integrate your own tweet scraping service for real-time social media monitoring.

### Database Management
- **Creator Tracking**: Persistent storage of token creator information
- **Post Deduplication**: Prevents duplicate analysis of the same posts
- **Historical Data**: Maintains trading history and performance metrics

### API Integration
- **Jupiter Price API**: Real-time token pricing and market data
- **Solana RPC**: Direct blockchain interaction for wallet operations
- **Chart Generation**: Automated price chart creation via QuickChart

## 🤗 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📊 Architecture

```
cracked-trading-bot/
├── app/
│   ├── bot_controller/     # Telegram bot management
│   ├── core/              # Configuration and logging
│   ├── handlers/          # Bot command handlers
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic and integrations
│   ├── repository/        # Data persistence layer
│   ├── utils/             # Utility functions
│   └── static/            # Static data and prompts
├── scripts/               # Setup and deployment scripts
└── requirements.txt       # Python dependencies
```

## 🔮 Future Enhancements

- **Advanced Analytics**: Portfolio performance tracking and analytics dashboard
- **Machine Learning**: Historical pattern recognition for improved predictions
- **Social Sentiment**: Integration with multiple social media platforms
- **Risk Management**: Advanced position sizing and stop-loss mechanisms

## ⚠️ Disclaimer

This bot is for educational purposes only. Cryptocurrency trading involves significant risk. Always do your own research and never invest more than you can afford to lose. The developers are not responsible for any financial losses incurred through the use of this software.

## ✍️ Acknowledgments

This project wouldn't be possible without these amazing technologies:
- [Believe.app](https://believe.app/) - Token launch platform
- [Solana](https://solana.com/) - High-performance blockchain platform
- [Jupiter](https://jup.ag/) - Solana's key liquidity aggregator
- [OpenAI GPT-4](https://openai.com/) - Advanced AI for trading decisions
- [Aiogram](https://docs.aiogram.dev/) - Modern Telegram Bot framework

