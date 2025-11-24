# main.py
"""
Application entry point for Blue Whisper Ocean Club Telegram Bot.
Initializes and launches the Telegram bot with proper error handling.
"""

import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from config.env_config import EnvConfigLoader
from adapters.telegram_adapter import TelegramBotAdapter


async def main() -> int:
    """
    Main application entry point for Telegram bot.

    Returns:
        Exit status code (0 for success, 1 for error)
    """
    try:
        # Load environment variables
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)

        print("🚀 Starting Blue Whisper Ocean Club Telegram Bot...\n")

        # Load and validate configuration
        config = EnvConfigLoader.load()

        if not EnvConfigLoader.validate_token(config.telegram_bot_token):
            raise ValueError("Invalid Telegram bot token format")

        # Initialize Telegram adapter
        bot = TelegramBotAdapter(config.telegram_bot_token)

        # Start bot
        await bot.start()

        # Keep running until interrupted
        print("\n⚡ Press Ctrl+C to stop the bot\n")

        # Run forever
        await asyncio.Event().wait()

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down bot gracefully...")
        return 0

    except ValueError as e:
        print(f"\n❌ Configuration error: {str(e)}")
        print("\nPlease check your .env file and try again.\n")
        return 1

    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print("Please contact support if the problem persists.\n")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
