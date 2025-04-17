#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA v2.0 — Final Webhook Edition
Stable Architecture | Telegram + Flask + Gunicorn
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

# === Modules ===
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# === Constants ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment variables.")

WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# === Logging ===
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("novaxa")

# === Flask App ===
flask_app = Flask(__name__)
bot = Bot(token=TOKEN)

# === Telegram Application ===
application: Application = ApplicationBuilder().token(TOKEN).build()

# === Core Initialization Function ===
async def init_bot():
    await application.initialize()
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    logger.info("Webhook set and bot initialized.")

# === Webhook Endpoint ===
@flask_app.post("/webhook")
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        await application.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return f"Error: {str(e)}", 500

# === Manual Webhook Set Route ===
@flask_app.get("/setwebhook")
def set_webhook():
    try:
        asyncio.run(init_bot())
        return "Webhook set successfully.", 200
    except Exception as e:
        return f"Webhook setup failed: {e}", 500

# === Telegram Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOVAXA v2.0 is now running with webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: NOVAXA v2.0 online and stable.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# === Core Class (Modular Design) ===
class EnhancedBot:
    def __init__(self):
        self.api = TelegramAPI(TOKEN)
        self.integration = ServiceIntegration()
        self.notification = NotificationSystem()
        self.monitor = SystemMonitor()
        self.performance = PerformanceTracker()
        self.user_sessions = {}
        self.user_settings = {}

# === Entrypoint for Gunicorn ===
app = flask_app
