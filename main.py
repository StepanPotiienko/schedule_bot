import asyncio
import datetime
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
)

from bot_logger import BotLogger
from date import Date

logger = BotLogger()

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


is_running: bool = False


# TODO: Everyday or specific date remainder.
# TODO: User configures time when a notification should be sent by bot.
# TODO: Appending info to a notification for example URL.


async def start(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 Hello! I am your scheduling assistant.\n\n📅 You can use me to schedule events, ⏰ set reminders, and ✅ manage your daily tasks.\n\nCommands:\n/start - Get this welcome message\n/set_hourly_remainder {every n hours} - Add a new remainder which will be executed every n hours.\n\n\n\nLet’s get started!"
    )


class HabitType:
    types: list = ["Work", "Personal", "Relationships"]

    def __init__(self, type: str):
        if type in self.types:
            self.type = type

    def get(self):
        return self.type

    def append(self, type: str):
        self.types.append(type)


class Habit:
    def __init__(self, name: str, priority: int, type: HabitType):
        self.name = name
        # 0 - highest
        self.priority = priority
        self.type = type
        # 😢 - not completed, 😀 - completed
        self.is_completed = False

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type.get()

    def mark_completed(self):
        self.is_completed = True

    def check_if_completed(self):
        if self.is_completed == True:
            return "😀"
        else:
            return "😢"


async def habit_tracker(update: Update, _: CallbackContext):
    # Each day user should mark a habit as 'complete' in order
    # to not lose the streak.
    habits: list = []
    habit: Habit = Habit("Read a book", 1, HabitType("Work"))
    habit2: Habit = Habit("Clean keyboard", 1, HabitType("Personal"))
    habit2.mark_completed()

    habits.append(habit)
    habits.append(habit2)

    for i in range(len(habits)):
        await update.message.reply_text(
            habits[i].check_if_completed()
            + " : "
            + habits[i].get_name()
            + " - "
            + habits[i].get_type(),
            parse_mode="HTML",
        )


def fetch_arguments(update: Update):
    args = update.message.text.split(" ")

    if len(args) > 1:
        return args[1]

    else:
        logger.error("Cannot obtain value.")
        return "❌ Cannot obtain value. Please try again and provide one."


# How to properly handle periods?
# How do I know if user wants to set every week,
# everyday, or every hour remainder?
async def set_hourly_schedule(update: Update, _: CallbackContext) -> None:
    try:
        period = fetch_arguments(update)
        period = float(period)
    except ValueError:
        await update.message.reply_text(period)
        return

    await update.message.reply_text("✅ The alarm has been successfully set up.")

    async def alarm_loop():
        while True:
            await asyncio.sleep(period * 3600)
            await update.message.reply_text("🔔 The alarm has gone off!")

    asyncio.create_task(alarm_loop())


async def add_event(update: Update, _: CallbackContext) -> None:
    args = update.message.text.split(" ")
    date: str = ""

    if len(args) > 1:
        date = datetime.datetime.strptime(args[1], "%d%m%Y").date()
        print(date)
    else:
        logger.error("Cannot obtain 'date' value.")
        await update.message.reply_text(
            "❌ Cannot obtain 'date' value. Please try again and provide one."
        )

        return

    await update.message.reply_text("✅ The remainder has been set up successfully.")

    # TODO: Separate thread.
    if date == datetime.date.today():
        # Notify user.
        await update.message.reply_text("🔔 The date is today!")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_event", add_event))
    app.add_handler(CommandHandler("set_hourly_remainder", set_hourly_schedule))
    app.add_handler(CommandHandler("habit_tracker", habit_tracker))

    logger.info("Application started.")
    app.run_polling()

    # Polling ends only on application termination
    # so the next lines of code execute on exit.
    logger.info("Application terminated.")


if __name__ == "__main__":
    main()
