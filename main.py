import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import BOT_TOKEN

BASE_PATH = "anime"

def get_anime_list():
    return {
        anime.lower(): anime
        for anime in os.listdir(BASE_PATH)
        if os.path.isdir(os.path.join(BASE_PATH, anime))
    }

def get_seasons(anime):
    path = os.path.join(BASE_PATH, anime)
    return [s for s in os.listdir(path) if os.path.isdir(os.path.join(path, s))]

def get_episodes(anime, season):
    path = os.path.join(BASE_PATH, anime, season)
    return [e for e in os.listdir(path) if e.endswith(".txt")]

def get_episode_link(anime, season, episode):
    path = os.path.join(BASE_PATH, anime, season, episode)
    with open(path, "r", encoding="utf-8") as f:
        return f.readline().strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    anime_map = get_anime_list()

    if text in anime_map:
        anime = anime_map[text]
        seasons = get_seasons(anime)

        keyboard = [
            [InlineKeyboardButton(s.replace("_", " "), callback_data=f"A|{anime}|{s}")]
            for s in seasons
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

    data = query.data.split("|")

    if data[0] == "A":
        _, anime, season = data
        episodes = get_episodes(anime, season)

        keyboard = [
            [InlineKeyboardButton(
                e.replace(".txt", "").replace("_", " "),
                callback_data=f"E|{anime}|{season}|{e}"
            )]
            for e in episodes
        ]

        await query.edit_message_text(
            "🎬 Select Episode:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data[0] == "E":
        _, anime, season, episode = data
        link = get_episode_link(anime, season, episode)

        await query.edit_message_text(
            "▶ Click below to watch episode",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("▶ Watch Episode", url=link)]
            ])
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🤖 Folder-based Anime Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
