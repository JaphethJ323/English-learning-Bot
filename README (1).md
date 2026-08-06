# MEME_HUB.exe — Telegram Bot

A joke/meme/GIF-topic Telegram bot built with `python-telegram-bot`.

## Files in this repo

| File | Purpose |
|---|---|
| `bot.py` | The bot itself |
| `requirements.txt` | Python dependencies |
| `Procfile` | Tells Railway how to start the bot (`worker: python bot.py`) |
| `.gitignore` | Keeps `.env` and other junk out of git |
| `.env.example` | Shows which env var to set — copy to `.env` for local testing, never commit the real one |

## 1. Get a bot token

1. Open Telegram, message **@BotFather**.
2. Send `/newbot` and follow the prompts.
3. Copy the token it gives you (looks like `123456789:AAExampleTokenAbc`).

## 2. Push this folder to GitHub

```bash
cd memehub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Because `.env` is gitignored and the token is never hardcoded in `bot.py`, it's safe to make this repo public.

## 3. Deploy on Railway

1. Go to [railway.app](https://railway.app) and log in.
2. **New Project → Deploy from GitHub repo** → select this repo.
3. Once it's created, open the service → **Variables** tab → add:
   - `BOT_TOKEN` = the token from BotFather
4. Open the **Settings** tab and confirm the **Start Command** is `python bot.py` (Railway usually picks this up automatically from the `Procfile`).
5. Railway will build and deploy automatically. Check the **Deployments → Logs** tab — you should see:
   ```
   🌃 MEME_HUB.exe Bot is starting...
   ```
6. Message your bot on Telegram and try `/start`.

## Notes

- This uses **long polling** (`run_polling`), so no public URL/webhook is required — it just needs to stay running, which Railway's worker process handles.
- If you ever regenerate the bot token in BotFather, update the `BOT_TOKEN` variable in Railway's dashboard — no code changes needed.
- Local testing: `pip install -r requirements.txt`, create a `.env` from `.env.example`, export it (`export $(cat .env | xargs)` on Mac/Linux), then `python bot.py`.
