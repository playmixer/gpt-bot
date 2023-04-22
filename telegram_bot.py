import os
from core import telegram

TELEGRAM_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if __name__ == "__main__":
    bot = telegram.TelegramBot(
        telegram_api_key=TELEGRAM_API_KEY,
        openai_api_key=OPENAI_API_KEY,
        replicate_api_key=REPLICATE_API_TOKEN
    )
    bot.run()
