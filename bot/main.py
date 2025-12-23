"""Telegram Markdown Processor Bot"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import ApplicationConfig
from utils import (
    setup_logger,
    validate_markdown_input,
    format_user_info,
    send_status_message,
)

ApplicationConfig.validate_config()
logger = setup_logger()


class MarkdownBotProcessor:
    WELCOME_MESSAGE = (
        "🎯 *Welcome to Markdown Processor Bot\\!*\n\n"
        "📝 Send Markdown text \\- get Telegram markup\n\n"
        "• /help \\- commands\n"
        "• /about \\- info"
    )

    HELP_MESSAGE = (
        "*Commands:*\n\n"
        "/start \\- start\n"
        "/help \\- this help\n"
        "/about \\- about bot\n"
        "/reset \\- clear history\n\n"
        "*Markdown syntax:*\n"
        "\\*\\*bold\\*\\* \\| \\*italic\\* \\| \\`code\\`"
    )

    ABOUT_MESSAGE = (
        "*Markdown Processor Bot v2\\.0*\n\n" "Convert Markdown to Telegram markup"
    )

    def __init__(self):
        self.logger = logger

    async def handle_start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user_info = format_user_info(update)
        self.logger.info(f"User {user_info} started bot")
        await send_status_message(
            update, context, self.WELCOME_MESSAGE, use_markdown=True
        )

    async def handle_help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        self.logger.info(f"Help requested by {format_user_info(update)}")
        await send_status_message(update, context, self.HELP_MESSAGE, use_markdown=True)

    async def handle_about_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        self.logger.info(f"About requested by {format_user_info(update)}")
        await send_status_message(
            update, context, self.ABOUT_MESSAGE, use_markdown=True
        )

    async def handle_reset_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user_info = format_user_info(update)
        self.logger.info(f"History cleared by {user_info}")
        context.user_data.clear()
        await send_status_message(
            update, context, "✅ History cleared\\.", use_markdown=True
        )

    async def process_markdown_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user_message = update.message.text
        user_info = format_user_info(update)

        is_valid, error_msg = validate_markdown_input(user_message)
        if not is_valid:
            self.logger.warning(f"Invalid input from {user_info}: {error_msg}")
            await send_status_message(
                update, context, f"⚠️ {error_msg}", use_markdown=False
            )
            return

        try:
            await update.message.reply_markdown_v2(user_message)
            self.logger.info(
                f"Message processed from {user_info} ({len(user_message)} chars)"
            )
        except Exception as e:
            self.logger.error(f"Markdown error for {user_info}: {e}", exc_info=True)
            await send_status_message(
                update,
                context,
                "❌ Markdown error\\. Check syntax\\.",
                use_markdown=True,
            )


class BotApplication:
    def __init__(self, token: str):
        self.token = token
        self.application = None
        self.processor = MarkdownBotProcessor()
        self.logger = logger

    def _setup_handlers(self) -> None:
        if not self.application:
            raise RuntimeError("App not initialized")

        self.application.add_handler(
            CommandHandler("start", self.processor.handle_start_command)
        )
        self.application.add_handler(
            CommandHandler("help", self.processor.handle_help_command)
        )
        self.application.add_handler(
            CommandHandler("about", self.processor.handle_about_command)
        )
        self.application.add_handler(
            CommandHandler("reset", self.processor.handle_reset_command)
        )
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, self.processor.process_markdown_message
            )
        )

    def initialize(self):
        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()
        self.logger.info("Bot initialized")
        return self

    def run(self) -> None:
        if not self.application:
            raise RuntimeError("App not initialized")

        self.logger.info("🚀 Bot started")
        self.logger.info(f"Config: {ApplicationConfig.get_config_summary()}")

        try:
            self.application.run_polling(
                allowed_updates=None, drop_pending_updates=True
            )
        except KeyboardInterrupt:
            self.logger.info("Bot stopped")
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)
            raise


def main() -> None:
    try:
        bot = BotApplication(token=ApplicationConfig.TELEGRAM_BOT_TOKEN)
        bot.initialize()
        bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
