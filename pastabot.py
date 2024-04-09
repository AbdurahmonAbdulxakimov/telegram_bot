from dotenv import load_dotenv
import os
import json
import telegram
from telegram import ReplyKeyboardMarkup, Update, Location
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


load_dotenv()

TOKEN = os.environ.get("TOKEN")
(FIKR_BILDIRISH,) = range(1)
MENU = "🍴 Menyu"
BASKET = "📥 Savat"
LOCATION = "KAFE LOKATSIYASI"
ABOUT_ORDER = "🚀 Buyurtma haqida"
FEEDBACK = "✍️ Fikr bildirish"
CONTACT = "☎️ Kontaktlar"
MAIN_KEYBOARD = [
    [MENU, BASKET],
    [LOCATION, ABOUT_ORDER],
    [FEEDBACK, CONTACT],
]
MARKS = [["Zo'r 5"], ["Yaxshi 4"], ["O'rtacha 3"], ["Qoniqarsiz 2"], ["Yomon 1"]]


def start(update: Update, context: CallbackContext) -> None:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "«CIAO!»  Abdurahmon! Kichik Italiyaga xush kelibsiz 🇮🇹\n"
        "Nima buyurtma qilamiz?",
        reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD),
    )


def about_order(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "🇮🇹 Italiyani yetkazib berish!\n"
        "🍝 Italiyancha pasta korobochkalarda!\n"
        "⏰ С 11:00 до 01:00 \n"
        "🛵 Hoziroq buyurtma bering!\n\n"
        "*Ob havo va yo'l tirbandliklar sababli yetkazish narxi o'zgarishi mumkin",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
        ),
    )


def location(update: Update, context: CallbackContext) -> None:
    update.message.reply_location(latitude=41.312082, longitude=69.292853)
    update.message.reply_text(
        "🤩 Pastani kafeimizga kelib to'g'ridan-to'g'ri skovorodkadan ta'tib ko'ring - aynan shu uchun ham shaharning markazida joy ochdik, manzil Ц-1'da Ecopark va 64 maktab yonida\n"
        "📌 Ish tartibi: du - pa 11:00 - 23:00 / ju 14:00 - 23:00 / sha - yak 11:00 - 23:00\n\n"
        "Operator bilan aloqa 👉 @pastarobot",
        reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD),
    )


def feedback(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "✅ PASTA-PASTA ni tanlaganingiz uchun rahmat.\n"
        "Agar Siz bizning xizmatlarimiz sifatini yaxhshilashga yordam bersangiz benihoyat hursand bo’lamiz.\n"
        "Buning uchun 5 ballik tizim asosida bizni baholang\n",
        reply_markup=ReplyKeyboardMarkup(MARKS),
    )
    return FIKR_BILDIRISH


def marking(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        """Bahoyingiz uchun rahmat""",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            one_time_keyboard=False,
            input_field_placeholder="Quyidagilardan birini tanlang",
        ),
    )
    return ConversationHandler.END


def contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Buyurtma va boshqa savollar bo'yicha javob olish uchun @pastarobot'ga murojaat qiling, barchasiga javob beramiz :)",
        reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD),
    )


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(Filters.text(ABOUT_ORDER), about_order),
            MessageHandler(Filters.text(LOCATION), location),
            MessageHandler(Filters.text(FEEDBACK), feedback),
            MessageHandler(Filters.text(CONTACT), contact),
        ],
        states={
            FIKR_BILDIRISH: [
                MessageHandler(Filters.regex("^(Zo'r 5|Yaxshi 4)$"), marking)
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            MessageHandler(Filters.text(ABOUT_ORDER), about_order),
            MessageHandler(Filters.text(LOCATION), location),
            MessageHandler(Filters.text(FEEDBACK), feedback),
            MessageHandler(Filters.text(CONTACT), contact),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
