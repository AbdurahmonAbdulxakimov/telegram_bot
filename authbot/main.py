# Python-telegram-bot Apps
from telegram import Bot
from telegram.ext import Updater

# Third Party Apps
from dotenv import load_dotenv
import os

# Local Apps
from sys_commands import set_up_commands
from handler import conv_handler


def main():
    load_dotenv("./.env")

    # Create the Bot
    bot = Bot(os.environ.get("TOKEN"))

    # Create the Updater
    updater = Updater(bot=bot)

    # Setup dispatcher
    dispatcher = updater.dispatcher

    # Setup commands
    set_up_commands(bot)

    # Register Handlers
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
