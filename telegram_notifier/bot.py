import os
from pathlib import Path

import dotenv
from telebot import TeleBot


def send_file():
    dotenv.load_dotenv()
    telegram_bot = TeleBot(os.getenv("TELEGRAM_BOT_ACCESS_TOKEN"))
    file_path = Path(__file__).parents[1] / "swagger-coverage-dm-api-account.html"
    with open(file_path, "rb") as document:
        telegram_bot.send_document(
            os.getenv("TELEGRAM_BOT_CHAT_ID"),
            document=document,
            caption="coverage",
        )


if __name__ == "__main__":
    send_file()
