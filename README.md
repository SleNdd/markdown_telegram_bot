# Markdown Processor Bot

Simple Telegram bot for converting Markdown to Telegram markup.

## Features

- 📝 Convert Markdown to Telegram markup
- 🔧 Multiple commands: `/start`, `/help`, `/about`, `/reset`
- 🛡️ Input validation and error handling
- 🐳 Docker ready
- ⚡ Fast and lightweight

## Quick Start

### Local setup

```bash
# Clone & setup
git clone <repo>
cd markdown_bot
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Install & run
pip install -r requirements.txt
echo "TELEGRAM_TOKEN=your_token" > .env
python -m bot.main
```

### Docker

```bash
echo "TELEGRAM_TOKEN=your_token" > .env
docker-compose up -d
```

## Commands

- `/start` - Welcome
- `/help` - Help & syntax
- `/about` - Bot info
- `/reset` - Clear history

## Requirements

- Python 3.11+
- Telegram Bot API token

## Config

Set in `.env`:
```
TELEGRAM_TOKEN=your_token_here
DEBUG=False
LOG_LEVEL=INFO
```

## License

MIT
