"""
Application entry point for Blue Whisper Ocean Club Telegram Bot.
Production-ready with comprehensive error handling and logging.
"""

import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from config.env_config import EnvConfigLoader
from adapters.telegram_adapter import TelegramBotAdapter


# Configure logging
def setup_logging():
    """Configure production-grade logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"bot_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )

    # Reduce telegram library logging
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)

    return logging.getLogger(__name__)


async def main() -> int:
    """
    Main application entry point for Telegram bot.

    Returns:
        Exit status code (0 for success, 1 for error)
    """
    logger = setup_logging()
    bot = None

    try:
        logger.info("=" * 60)
        logger.info("🚀 Starting Blue Whisper Ocean Club Telegram Bot")
        logger.info("=" * 60)

        # Load environment variables
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info("✅ Environment variables loaded from .env")
        else:
            logger.warning("⚠️  No .env file found, using system environment variables")

        # Load and validate configuration
        config = EnvConfigLoader.load()
        logger.info(f"✅ Configuration loaded (Environment: {config.environment})")

        if not EnvConfigLoader.validate_token(config.telegram_bot_token):
            raise ValueError("Invalid Telegram bot token format")

        logger.info("✅ Bot token validated")

        # Initialize Telegram adapter
        bot = TelegramBotAdapter(config.telegram_bot_token)
        logger.info("✅ Telegram adapter initialized")

        # Start bot
        await bot.start()
        logger.info("🤖 Bot started successfully")
        logger.info("✅ Bot is ready and listening for messages!")
        logger.info("⚡ Bot: @BlueWhisperOmanBot")
        logger.info("=" * 60)
        logger.info("📊 Bot Status: RUNNING")
        logger.info("🔄 Restart Policy: unless-stopped")
        logger.info("⏰ Timezone: Asia/Muscat")
        logger.info("=" * 60)

        # Keep running until interrupted
        logger.info("⚡ Press Ctrl+C to stop the bot\n")

        # Run forever
        await asyncio.Event().wait()

    except KeyboardInterrupt:
        logger.info("\n\n👋 Received shutdown signal...")
        logger.info("🛑 Shutting down bot gracefully...")
        if bot:
            await bot.stop()
        logger.info("✅ Bot stopped successfully")
        return 0

    except ValueError as e:
        logger.error(f"❌ Configuration error: {str(e)}")
        logger.error("Please check your .env file and try again.")
        return 1

    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}", exc_info=True)
        logger.error("Please contact support if the problem persists.")
        return 1

    finally:
        logger.info("=" * 60)
        logger.info("Bot shutdown complete")
        logger.info("=" * 60)


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
