import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
import os

# === CONFIGURA QUI ===
BOT_TOKEN = "7676180777:AAFCNMMAQ9Xv38k-WSKu0t7lDuSIUChg-Pk"
CHANNEL_USERNAME = "@scontipazzi"

# === LOGGING ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# === COMANDO /start ===
def start(update, context):
    update.message.reply_text("Ciao! Sono il bot ufficiale di Sconti Pazzi!")

# === COMANDO /offerta ===
def offerta(update, context):
    # Messaggio e link dell'offerta
    testo = "Offerta incredibile! Solo per oggi:\n\nSmartwatch a 29,99€!"
    link_offerta = "https://www.amazon.it/dp/PRODOTTO_FAKE"

    # Pulsante
    keyboard = [
        [InlineKeyboardButton("Vai all'offerta", url=link_offerta)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Pubblica sul canale
    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=teso,
        reply_markup=reply_markup
    )

    update.message.reply_text("Offerta pubblicata sul canale.")

# === MAIN ===
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("offerta", offerta))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
