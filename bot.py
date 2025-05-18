
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Simulated offers per category
offers = {
    "tecnologia": [
        ("Echo Dot 5ª gen", "39,99€", "https://amzn.to/echo-dot"),
        ("Cuffie Sony WH-1000XM4", "229,99€", "https://amzn.to/sony-xm4"),
        ("Fire TV Stick 4K", "44,99€", "https://amzn.to/fire-stick")
    ],
    "casa": [
        ("Aspirapolvere Rowenta", "99,99€", "https://amzn.to/rowenta"),
        ("Friggitrice ad aria", "69,99€", "https://amzn.to/friggitrice"),
        ("Lampada LED smart", "19,99€", "https://amzn.to/lampada")
    ],
    "moda": [
        ("Sneakers Nike", "74,99€", "https://amzn.to/nike"),
        ("Zaino Eastpak", "49,99€", "https://amzn.to/eastpak"),
        ("Occhiali da sole Ray-Ban", "89,99€", "https://amzn.to/rayban")
    ]
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Benvenuto su *ScontiPazzi*!\n\nScrivi /offerte per vedere le offerte del giorno\n"
        "Oppure esplora le categorie con /categorie",
        parse_mode='Markdown'
    )

async def aiuto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Benvenuto\n"
        "/offerte - Offerte generali\n"
        "/categorie - Vedi tutte le categorie\n"
        "/categoria [nome] - Offerte per categoria (es. /categoria tecnologia)"
    )

async def offerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "*Offerte del giorno:*\n\n"
    for nome, prezzo, link in offers["tecnologia"][:3]:
        msg += f"- [{nome}]({link}) — *{prezzo}*\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def categorie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(cat.capitalize(), callback_data=f"categoria_{cat}")]
        for cat in offers.keys()
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Scegli una categoria:", reply_markup=markup)

async def categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Scrivi il nome di una categoria, es. /categoria tecnologia")
        return
    cat = context.args[0].lower()
    if cat not in offers:
        await update.message.reply_text("Categoria non trovata.")
        return
    msg = f"*Offerte per {cat.capitalize()}:*\n\n"
    for nome, prezzo, link in offers[cat][:3]:
        msg += f"- [{nome}]({link}) — *{prezzo}*\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("categoria_"):
        cat = query.data.replace("categoria_", "")
        if cat in offers:
            msg = f"*Offerte per {cat.capitalize()}:*\n\n"
            for nome, prezzo, link in offers[cat][:3]:
                msg += f"- [{nome}]({link}) — *{prezzo}*\n"
            await query.edit_message_text(msg, parse_mode='Markdown')

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aiuto", aiuto))
    app.add_handler(CommandHandler("offerte", offerte))
    app.add_handler(CommandHandler("categorie", categorie))
    app.add_handler(CommandHandler("categoria", categoria))
    app.add_handler(telegram.ext.CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
