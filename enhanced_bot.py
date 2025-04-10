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

# Load token
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
logger = logging.getLogger("enhanced_bot")

# Init Application
application: Application = ApplicationBuilder().token(TOKEN).build()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to NOVAXA_BOT v2.0 — powered by webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Online and stable.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Core system (Manus structure)
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

# Set webhook route
@app.get("/setwebhook")
def set_webhook():
    try:
        webhook_url = "https://novaxa-v2-core.onrender.com/webhook"
        asyncio.run(bot.delete_webhook())
        result = asyncio.run(bot.set_webhook(url=webhook_url))
        logger.info("Webhook set successfully.")
        return f"Webhook set: {result}", 200 if result else 400
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        return f"Error setting webhook: {str(e)}", 500

# Entrypoint for Gunicorn
app.run = lambda **kwargs: application.run_polling()  # fallback if gunicorn fails

app_instance = app  # for gunicorn: `gunicorn enhanced_bot:app_instance --bind 0.0.0.0:$PORT`