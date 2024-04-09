# Python-telegram-bot Apps
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from . import static_text
from . import keyboards


class Choices:
    CONTACT, LOCATION = range(2)


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        static_text.starting_text,
        reply_markup=keyboards.contact_markup,
    )

    return Choices.CONTACT


def contact(update: Update, context: CallbackContext) -> int:
    context.user_data["contact"] = update.message.contact
    update.message.reply_text(
        static_text.request_location,
        reply_markup=keyboards.location_markup,
    )

    return Choices.LOCATION


def location(update: Update, context: CallbackContext) -> None:
    context.user_data["location"] = update.message.location
    update.message.reply_text(
        f"Your Phone Number is: {context.user_data['contact'].phone_number}\n"
        f"Location is in {context.user_data['location'].latitude}, {context.user_data['location'].longitude}\n",
        reply_markup=ReplyKeyboardRemove(),
    )
