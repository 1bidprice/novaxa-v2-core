#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA v2.0 — Enhanced Webhook Bot (Flask)
Manus Design + FIXED initialize() and start()
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

# === Environment ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set.")

WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# === Flask App ===
app = Flask(__name__)
bot = Bot(token=TOKEN)

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enhanced_bot")

# === Application ===
application: Application = ApplicationBuilder().token(TOKEN).build()

# === Init Core ===
class EnhancedBot:
    def __init__(self):
        self.api = TelegramAPI(TOKEN)
        self.integration = ServiceIntegration()
        self.notification = NotificationSystem()
        self.monitor = SystemMonitor()
        self.performance = PerformanceTracker()
        self.user_sessions = {}
        self.user_settings = {}

core = EnhancedBot()

# === Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOVAXA v2.0 — Ready via Webhook!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: ONLINE and responding.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# === Webhook endpoint ===
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

# === Startup Hook ===
@app.before_first_request
def initialize_bot():
    asyncio.get_event_loop().create_task(async_startup())

async def async_startup():
    await application.initialize()
    await application.start()
    await bot.delete_webhook()
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info("Webhook initialized and bot started.")

# === Gunicorn Entrypoint ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
