# Python-telegram-bot Apps
from telegram import ReplyKeyboardMarkup, KeyboardButton

contact_markup = ReplyKeyboardMarkup(
    [[KeyboardButton("☎️ Contact", request_contact=True)]],
)

location_markup = ReplyKeyboardMarkup(
    [[KeyboardButton("📍 Location", request_location=True)]],
)
