import os
import random
import logging
from datetime import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ─── CONFIG ───────────────────────────────────────────────
# The bot token is read from an environment variable so it never
# has to be committed to GitHub. Set BOT_TOKEN in Railway's
# "Variables" tab (see README.md).
BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── DATA ─────────────────────────────────────────────────
JOKES = [
    ("Why don't scientists trust atoms?", "Because they make up everything!"),
    ("Why did the scarecrow win an award?", "He was outstanding in his field!"),
    ("Why don't skeletons fight each other?", "They don't have the guts!"),
    ("What do you call a fake noodle?", "An impasta!"),
    ("Why did the bicycle fall over?", "It was two tired!"),
    ("What do you call cheese that isn't yours?", "Nacho cheese!"),
    ("Why can't you give Elsa a balloon?", "Because she'll let it go!"),
    ("What do you call a bear with no teeth?", "A gummy bear!"),
    ("Why did the math book look sad?", "Because it had too many problems."),
    ("What do you call a sleeping dinosaur?", "A dino-snore!"),
    ("Why did the tomato turn red?", "Because it saw the salad dressing!"),
    ("What do you call a fish with no eyes?", "Fsh!"),
    ("Why did the cookie go to the doctor?", "Because it felt crummy."),
    ("What do you call a can opener that doesn't work?", "A can't opener!"),
    ("Why did the golfer bring two pairs of pants?", "In case he got a hole in one!"),
]

TRENDING_TOPICS = [
    "🐱 Cat memes never die — 12.4k laughs",
    "🤖 AI doing human things — 9.8k laughs",
    "☕ Monday mood be like — 15.2k laughs",
    "🐶 Doggo did a zoomie — 18.1k laughs",
    "🍕 Pineapple on pizza war — 22.3k laughs",
    "😴 Me pretending to work — 11.7k laughs",
    "🦄 Expectation vs Reality — 14.5k laughs",
    "🌮 Taco Tuesday energy — 16.9k laughs",
    "🎮 Just one more game — 20.1k laughs",
    "🌈 Relatable millennial memes — 13.3k laughs",
]

MEME_TEMPLATES = [
    "🖼️ Distracted Boyfriend — When you see a new meme format",
    "🖼️ Drake Hotline Bling — Approving the good stuff",
    "🖼️ Expanding Brain — Levels of humor enlightenment",
    "🖼️ Woman Yelling at Cat — The eternal debate",
    "🖼️ Always Has Been — Wait, it's all memes?",
    "🖼️ Doge — Much wow, very laugh",
    "🖼️ Two Buttons — The hardest choices require the strongest wills",
    "🖼️ Change My Mind — Memes are the highest form of art",
]

GIF_CATEGORIES = [
    "🎬 Laughing GIF — When the joke hits just right",
    "🎬 Facepalm GIF — When the meme is too relatable",
    "🎬 Dancing GIF — Celebrating a viral post",
    "🎬 Crying GIF — Laughing so hard you cry",
    "🎬 Thumbs Up GIF — Approval from the meme gods",
    "🎬 Mind Blown GIF — When the punchline drops",
    "🎬 Slow Clap GIF — Respect for elite humor",
    "🎬 Confused GIF — When you don't get the meme",
]

# ─── KEYBOARD MARKUP ──────────────────────────────────────
def main_menu():
    keyboard = [
        [InlineKeyboardButton("😂 Random Joke", callback_data="joke"),
         InlineKeyboardButton("🖼️ Random Meme", callback_data="meme")],
        [InlineKeyboardButton("🎬 Random GIF", callback_data="gif"),
         InlineKeyboardButton("🔥 Trending", callback_data="trending")],
        [InlineKeyboardButton("📅 Daily Joke (Subscribe)", callback_data="subscribe"),
         InlineKeyboardButton("❓ Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ─── TEXT BUILDERS (MarkdownV2-safe) ──────────────────────
def joke_text():
    setup, punchline = random.choice(JOKES)
    setup = escape_markdown(setup, version=2)
    punchline = escape_markdown(punchline, version=2)
    return f"😂 *{setup}*\n\n||{punchline}||"

def meme_text():
    meme = escape_markdown(random.choice(MEME_TEMPLATES), version=2)
    return f"🖼️ *Meme of the Moment*\n\n{meme}\n\n_Reply with your own caption\\!_"

def gif_text():
    gif = escape_markdown(random.choice(GIF_CATEGORIES), version=2)
    return f"🎬 *GIF Vibe Check*\n\n{gif}\n\n_\\(Imagine this looping infinitely\\)_"

def trending_text():
    topics = random.sample(TRENDING_TOPICS, 5)
    lines = "\n".join(f"• {escape_markdown(t, version=2)}" for t in topics)
    return f"🔥 *VIRAL FEED :: LIVE*\n\n{lines}"

def help_text():
    return (
        "🌃 *MEME\\_HUB\\.exe Help*\n\n"
        "I'm your daily humor bot\\. Here's how to use me:\n\n"
        "• Tap the buttons below for quick actions\n"
        "• Use /commands for a full command list\n"
        "• Subscribe to /daily for a joke every morning\n\n"
        "_Stay laughing\\. Stay viral\\._"
    )

# ─── COMMANDS ─────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = escape_markdown(user.first_name, version=2)
    welcome_text = (
        f"🌃 *Welcome to MEME\\_HUB\\.exe, {name}\\!*\n\n"
        f"```\nSYSTEM STATUS: ONLINE\nHUMOR_LEVELS: OPTIMAL\nPROTOCOL: DAILY_LAUGHS\n```\n\n"
        f"I deliver daily memes, jokes, GIFs, and viral humor\\.\n"
        f"Choose an option below or use /commands to see all commands\\."
    )
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=main_menu()
    )

async def commands_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📋 *Available Commands:*\n\n"
        "`/start` — Launch the bot\n"
        "`/joke` — Get a random joke\n"
        "`/meme` — Get a trending meme topic\n"
        "`/gif` — Get a GIF category\n"
        "`/trending` — See what's viral now\n"
        "`/daily` — Subscribe to daily jokes\n"
        "`/stop` — Unsubscribe from daily jokes\n"
        "`/help` — Show this help message"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def joke_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(joke_text(), parse_mode=ParseMode.MARKDOWN_V2)

async def meme_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(meme_text(), parse_mode=ParseMode.MARKDOWN_V2)

async def gif_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(gif_text(), parse_mode=ParseMode.MARKDOWN_V2)

async def trending_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(trending_text(), parse_mode=ParseMode.MARKDOWN_V2)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(help_text(), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())

# ─── CALLBACK HANDLERS ────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "joke":
        await query.edit_message_text(joke_text(), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())
    elif data == "meme":
        await query.edit_message_text(meme_text(), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())
    elif data == "gif":
        await query.edit_message_text(gif_text(), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())
    elif data == "trending":
        await query.edit_message_text(trending_text(), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())
    elif data == "subscribe":
        chat_id = query.message.chat_id
        job_name = f"daily_{chat_id}"

        current_jobs = context.job_queue.get_jobs_by_name(job_name)
        for job in current_jobs:
            job.schedule_removal()

        context.job_queue.run_daily(
            send_daily_joke,
            time=time(9, 0),
            days=(0, 1, 2, 3, 4, 5, 6),
            chat_id=chat_id,
            name=job_name
        )

        text = (
            "📅 *Daily Joke Subscribed\\!*\n\n"
            "You'll receive a fresh joke every day at *09:00*\\.\n\n"
            "Use `/stop` to unsubscribe anytime\\."
        )
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())
    elif data == "help":
        await query.edit_message_text(help_text(), parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_menu())

# ─── DAILY JOKE JOB ───────────────────────────────────────
async def send_daily_joke(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    text = f"📅 *Daily Dose of Laughter*\n\n{joke_text()}\n\n_Type /daily to subscribe or /stop to unsubscribe\\._"
    await context.bot.send_message(job.chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2)

async def daily_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    job_name = f"daily_{chat_id}"

    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    context.job_queue.run_daily(
        send_daily_joke,
        time=time(9, 0),
        days=(0, 1, 2, 3, 4, 5, 6),
        chat_id=chat_id,
        name=job_name
    )

    await update.message.reply_text(
        "📅 *Subscribed to Daily Jokes\\!*\n\n"
        "You'll get a fresh joke every day at *09:00*\\.\n"
        "Use `/stop` to unsubscribe\\.",
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    job_name = f"daily_{chat_id}"

    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
        await update.message.reply_text("✅ Unsubscribed. No more daily jokes.")
    else:
        await update.message.reply_text("ℹ️ You weren't subscribed to daily jokes.")

# ─── ERROR HANDLER ────────────────────────────────────────
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ SYSTEM ERROR — Something went wrong. Try again!"
        )

# ─── MAIN ─────────────────────────────────────────────────
def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Set it in Railway's Variables tab (or a local .env file)."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands_cmd))
    application.add_handler(CommandHandler("joke", joke_cmd))
    application.add_handler(CommandHandler("meme", meme_cmd))
    application.add_handler(CommandHandler("gif", gif_cmd))
    application.add_handler(CommandHandler("trending", trending_cmd))
    application.add_handler(CommandHandler("daily", daily_cmd))
    application.add_handler(CommandHandler("stop", stop_cmd))
    application.add_handler(CommandHandler("help", help_cmd))

    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_error_handler(error_handler)

    logger.info("🌃 MEME_HUB.exe Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
