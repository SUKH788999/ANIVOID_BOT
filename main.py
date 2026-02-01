import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from config import BOT_TOKEN

with open("anime_data.json", "r", encoding="utf-8") as f:
    ANIME_DATA = json.load(f)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in ANIME_DATA:
        keyboard = [
            [InlineKeyboardButton(season.title(), callback_data=f"{text}|{season}")]
            for season in ANIME_DATA[text]
        ]

        await update.message.reply_text(
            "📂 Select Season:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("❌ Anime available nahi hai")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    anime, season = query.data.split("|")
    episodes = ANIME_DATA[anime][season]

    keyboard = [
        [InlineKeyboardButton(ep.title(), url=link)]
        for ep, link in episodes.items()
    ]

    await query.edit_message_text(
        text=f"🎬 {season.title()} Episodes:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🤖 Anime Teleport Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
