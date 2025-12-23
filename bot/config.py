import os
from dotenv import load_dotenv

load_dotenv()


class ApplicationConfig:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    DEBUG_MODE: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_MESSAGE_LENGTH: int = 4096
    MAX_PROCESSING_TIME: int = 30

    @classmethod
    def validate_config(cls) -> None:
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_TOKEN not set")

    @classmethod
    def get_config_summary(cls) -> str:
        return (
            f"Debug: {cls.DEBUG_MODE}\n"
            f"Log: {cls.LOG_LEVEL}\n"
            f"Max: {cls.MAX_MESSAGE_LENGTH} chars"
        )
