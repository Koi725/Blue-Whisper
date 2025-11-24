🌊 Blue Whisper Ocean Club Bot

A professional, bilingual Telegram bot for Blue Whisper Ocean Club's water sports and activities booking system.
🎯 Features

    Bilingual Support: English & Arabic (Oman)
    Service Catalog: Jet Ski, Parasailing, Banana Boat, and more
    Direct WhatsApp Integration: Seamless booking redirection
    Social Media Links: Complete social presence
    Professional UI: Clean, intuitive conversation flow

🏗️ Architecture

blue-whisper-bot/
├── src/
│ ├── bot/ # Bot core logic
│ ├── models/ # Data models
│ ├── services/ # Business logic
│ ├── handlers/ # Message handlers
│ ├── utils/ # Utilities
│ └── config/ # Configuration
├── data/ # Static data files
├── tests/ # Unit tests
└── requirements.txt

🚀 Quick Start
bash

# Install dependencies

pip install -r requirements.txt

# Set environment variables

export TELEGRAM_BOT_TOKEN="your_token_here"
export WHATSAPP_NUMBER="+96812345678"

# Run the bot

python -m src.main

🛠️ Tech Stack

    Python 3.11+
    python-telegram-bot: Telegram Bot API
    Pydantic: Data validation
    python-dotenv: Environment management

📝 License

Proprietary - Blue Whisper Ocean Club © 2024
