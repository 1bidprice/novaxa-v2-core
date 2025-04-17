#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import asyncio
from flask import Flask, request

from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ContextTypes,
)

# === Logging ===
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("NOVAXA")

# === Load Token from Environment ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set.")

WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# === Flask App ===
flask_app = Flask(__name__)
app = flask_app  # For gunicorn

# === Telegram Application ===
telegram_app: Application = ApplicationBuilder().token(TOKEN).build()

# === Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOVAXA BOT v2.0 — online & secure!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Stable via webhook!")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("status", status))

# === Flask Webhook Route ===
@flask_app.post("/webhook")
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.initialize()
        await telegram_app.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return f"Error: {e}", 500

# === Manual Webhook Setup Route ===
@flask_app.get("/setwebhook")
def set_webhook():
    try:
        bot = Bot(token=TOKEN)

        async def setup():
            await bot.delete_webhook()
            result = await bot.set_webhook(url=WEBHOOK_URL)
            return result

        result = asyncio.run(setup())
        return f"Webhook set: {result}", 200
    except Exception as e:
        return f"Webhook setup error: {str(e)}", 500
