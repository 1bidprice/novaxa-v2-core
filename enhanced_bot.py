#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA_BOT v2.0 — Full Edition (Webhook + Modules)
Manus Spec — Secure TOKEN loading from environment
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

# Εσωτερικά modules
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# Φόρτωση TOKEN από περιβάλλον
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Init εφαρμογής Telegram
application: Application = ApplicationBuilder().token(TOKEN).build()

# Εντολές
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to NOVAXA_BOT v2.0 — powered by webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Online and stable.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands: /start, /status, /help")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("help", help_cmd))

# Κύρια Κλάση από Manus
class EnhancedBot:
    def __init__(self):
        self.api = TelegramAPI(TOKEN)
        self.integration = ServiceIntegration()
        self.notification = NotificationSystem()
        self.monitor = SystemMonitor()
        self.performance = PerformanceTracker()
        self.user_sessions = {}
        self.user_settings = {}

# Webhook route
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

# Ορισμός webhook
@app.get("/setwebhook")
def set_webhook():
    try:
        webhook_url = "https://novaxa-v2-core.onrender.com/webhook"
        bot.delete_webhook()
        result = bot.set_webhook(url=webhook_url)
        return f"Webhook set: {result}", 200 if result else 400
    except Exception as e:
        return f"Error setting webhook: {str(e)}", 500

# Εκκίνηση Flask + ενεργοποίηση Telegram app
if __name__ == "__main__":
    import asyncio

    async def main():
        await application.initialize()
        await application.start()
        await application.updater.start_polling()  # Required for message loop
        app.run(host="0.0.0.0", port=8080)

    asyncio.run(main())