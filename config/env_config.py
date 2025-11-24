import os
from dataclasses import dataclass


@dataclass
class EnvironmentConfig:
    telegram_bot_token: str
    environment: str = "production"
    debug_mode: bool = False


class EnvConfigLoader:
    @staticmethod
    def load() -> EnvironmentConfig:
        token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN not found in environment variables.\n"
                "Please create a .env file with your bot token."
            )

        environment = os.getenv("ENVIRONMENT", "production")
        debug_mode = os.getenv("DEBUG", "false").lower() == "true"

        return EnvironmentConfig(
            telegram_bot_token=token, environment=environment, debug_mode=debug_mode
        )

    @staticmethod
    def validate_token(token: str) -> bool:
        parts = token.split(":")
        return len(parts) == 2 and parts[0].isdigit() and len(parts[1]) > 30
