import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from config import ApplicationConfig


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        return logger

    logger.setLevel(getattr(logging, ApplicationConfig.LOG_LEVEL))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def validate_markdown_input(content: str) -> tuple[bool, Optional[str]]:
    if not content or not content.strip():
        return False, "Message is empty"
    if len(content) > ApplicationConfig.MAX_MESSAGE_LENGTH:
        return False, f"Max {ApplicationConfig.MAX_MESSAGE_LENGTH} chars"
    return True, None


def format_user_info(update: Update) -> str:
    user = update.effective_user
    return f"{user.first_name or 'User'} ({user.username or user.id})"


async def send_status_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    use_markdown: bool = False,
) -> None:
    try:
        if use_markdown:
            await update.message.reply_markdown_v2(text)
        else:
            await update.message.reply_text(text)
    except Exception as e:
        logging.getLogger(__name__).error(f"Message error: {e}")
