#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA v2.0 — Enhanced Webhook Bot (Flask)
Manus Design + FIXED initialize() issue
"""

import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import asyncio

# === System Modules ===
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# === Environment Variables ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set.")

WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# === Flask App ===
app = Flask(__name__)
bot = Bot(token=TOKEN)

# === Logging ===
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("enhanced_bot")

# === Telegram Application ===
application: Application = ApplicationBuilder().token(TOKEN).build()


# === Initialize ONCE ===
@app.before_first_request
def startup():
    """Runs once when the Flask app starts"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(bot.delete_webhook())
    loop.run_until_complete(bot.set_webhook(url=WEBHOOK_URL))
    logger.info("Bot initialized and webhook set.")


# === Telegram Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOVAXA v2.0 is active — powered by webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Online and stable.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))


# === Core Class (Manus Architecture) ===
class EnhancedBot:
    def __init__(self):
        self.api = TelegramAPI(TOKEN)
        self.integration = ServiceIntegration()
        self.notification = NotificationSystem()
        self.monitor = SystemMonitor()
        self.performance = PerformanceTracker()
        self.user_sessions = {}
        self.user_settings = {}


# === Webhook Endpoint ===
@app.post("/webhook")
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        await application.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return f"Error: {str(e)}", 500


# === Gunicorn Entrypoint ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
