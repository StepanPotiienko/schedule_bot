import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


def start_message() -> str:
    return "Hello! I am your bot. Send me a message, and I'll echo it back."


async def start(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(start_message())


async def echo(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()


if __name__ == "__main__":
    main()
