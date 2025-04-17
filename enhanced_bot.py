#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("enhanced_bot")

# Environment variables
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# Flask app
flask_app = Flask(__name__)
bot = Bot(token=TOKEN)

# Telegram Application
application: Application = ApplicationBuilder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to NOVAXA_BOT v2.0!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online and stable.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Initialize the Application (this was missing!)
asyncio.run(application.initialize())

# Webhook endpoint
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

# Route to manually set webhook
@flask_app.get("/setwebhook")
def set_webhook():
    try:
        async def setup():
            await bot.delete_webhook()
            return await bot.set_webhook(url=WEBHOOK_URL)
        result = asyncio.run(setup())
        return f"Webhook set: {result}", 200
    except Exception as e:
        return f"Error setting webhook: {str(e)}", 500

# Gunicorn entrypoint
app = flask_app
