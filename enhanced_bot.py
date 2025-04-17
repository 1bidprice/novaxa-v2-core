#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Εσωτερικές ενότητες
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("enhanced_bot")

# TOKEN & WEBHOOK
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN is not set.")

WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# Flask
flask_app = Flask(__name__)
bot = Bot(token=TOKEN)

# Application
application: Application = ApplicationBuilder().token(TOKEN).build()

# Ενεργοποίηση του application
import asyncio
asyncio.run(application.initialize())  # <-- ΚΡΙΣΙΜΟ

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to NOVAXA v2.0 via webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot status: Live and functional.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Core Modules
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
@flask_app.post("/webhook")
async def telegram_webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        await application.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return f"Error: {str(e)}", 500

# Set webhook manually
@flask_app.get("/setwebhook")
def set_webhook():
    try:
        import asyncio
        async def setup():
            await bot.delete_webhook()
            return await bot.set_webhook(url=WEBHOOK_URL)
        result = asyncio.run(setup())
        return f"Webhook set: {result}", 200
    except Exception as e:
        return f"Error setting webhook: {str(e)}", 500

# Render entrypoint
app = flask_app
