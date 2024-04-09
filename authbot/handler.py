# Python-telegram-bot Apps
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# Local Apps
from handlers import handlers
from handlers.handlers import Choices

# Add conversation handler
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", handlers.start),
    ],
    states={
        Choices.CONTACT: [
            MessageHandler(Filters.contact, handlers.contact),
        ],
        Choices.LOCATION: [
            MessageHandler(Filters.location, handlers.location),
        ],
    },
    fallbacks=[],
)
