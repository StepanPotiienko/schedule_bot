import os
from dotenv import load_dotenv
from logging import INFO
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

from bot_logger import BotLogger

logger = BotLogger()

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# TODO: Everyday or specific date remainder.
# TODO: User configures time when a notification should be sent by bot.
# TODO: Appending info to a notification for example URL.


async def start(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello! I am your scheduling assistant.\n\nYou can use me to schedule events, set reminders, and manage your daily tasks.\n\nCommands:\n/start - Get this welcome message\n/add_event - Add a new event\n/list_events - View all scheduled events\n/delete_event - Remove an event\n\nLet’s get started!"
    )


async def echo(update: Update, _: CallbackContext) -> None:
    logger.info(update.message.text)
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Application started.")
    app.run_polling()

    # Polling ends only on application termination
    # so the next lines of code execute on exit.
    logger.info("Application terminated.")


if __name__ == "__main__":
    main()
