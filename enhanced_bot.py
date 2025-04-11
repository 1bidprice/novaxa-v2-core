#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA_BOT v2.0 — Full Edition (Webhook + Modules)
Manus Spec — Secure TOKEN loading from environment
"""

import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Internal modules
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# Securely load token from environment
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Logging config
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("enhanced_bot")

# Init Telegram app
application: Application = ApplicationBuilder().token(TOKEN).build()

# Basic commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to NOVAXA_BOT v2.0 — powered by webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Online and stable.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Core enhanced class (from Manus)
class EnhancedBot:
    def __init__(self):
        self.api = TelegramAPI(TOKEN)
        self.integration = ServiceIntegration()
        self.notification = NotificationSystem()
        self.monitor = SystemMonitor()
        self.performance = PerformanceTracker()
        self.user_sessions = {}
        self.user_settings = {}

# Webhook endpoint
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

# Set webhook manually (fully async-safe in sync route)
@app.get("/setwebhook")
def set_webhook():
    try:
        webhook_url = "https://novaxa-v2-core.onrender.com/webhook"

        async def setup():
            await bot.delete_webhook()
            return await bot.set_webhook(url=webhook_url)

        result = asyncio.run(setup())
        logger.info("Webhook set successfully.")
        return f"Webhook set: {result}", 200 if result else 400
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        return f"Error setting webhook: {str(e)}", 500

# Entrypoint for gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
