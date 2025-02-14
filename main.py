import datetime
import asyncio
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


class Date:
    # Compare two datetime.date Objects.
    # Return the first one if greater, and the second one if not.
    def compare(first: datetime.date, second: datetime.date):
        if second <= first:
            return second
        else:
            return first

    def get_day(date: datetime.date):
        return date.day

    def get_month(date: datetime.date):
        return date.month

    def get_year(date: datetime.date):
        return date.year

    @staticmethod
    def get_current_date():
        return datetime.date.today()


async def start(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello! I am your scheduling assistant.\n\nYou can use me to schedule events, set reminders, and manage your daily tasks.\n\nCommands:\n/start - Get this welcome message\n/add_event - Add a new event\n/list_events - View all scheduled events\n/delete_event - Remove an event\n\nLet’s get started!"
    )


# How to properly handle periods?
# How do I know if user wants to set every week,
# everyday, or every hour remainder?
async def set_hourly_schedule(update: Update, _: CallbackContext, period: float = 1):
    if period < 1 or isinstance(period, int) == False:
        await update.message.reply_text("The number of hours can only be an integer.")
        return

    while True:
        await asyncio.sleep(period * 3600)
        await update.message.reply_text("The alarm has went off!")


async def get_current_date(update: Update, _: CallbackContext) -> None:
    date = Date()
    current_day = date.get_current_date()

    await update.message.reply_text("The current day is: " + str(current_day))


async def echo(update: Update, _: CallbackContext) -> None:
    logger.info(update.message.text)
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_current_day", get_current_date))
    app.add_handler(CommandHandler("set_hourly_remainder", set_hourly_schedule))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Application started.")
    app.run_polling()

    # Polling ends only on application termination
    # so the next lines of code execute on exit.
    logger.info("Application terminated.")


if __name__ == "__main__":
    main()
