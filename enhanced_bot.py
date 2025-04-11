#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA_BOT v2.0 — Webhook Edition
Manus Spec | Gunicorn Compatible | Render Web Service
"""

import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Internal Modules
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# Logging setup
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("enhanced_bot")

# Load token
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment variables")

# Webhook URL (Render)
WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# Build Application
application: Application = (
    ApplicationBuilder()
    .token(TOKEN)
    .webhook_url(WEBHOOK_URL)
    .build()
)

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Καλώς ήρθες στο NOVAXA_BOT v2.0 (Webhook Ready)!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Κατάσταση: Online και σε λειτουργία με webhook.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Core Modules from Manus
class EnhancedBot:
    def __init__(self):
        self.api = TelegramAPI(TOKEN)
        self.processor = DataProcessor()
        self.integration = ServiceIntegration()
        self.notification = NotificationSystem()
        self.monitor = SystemMonitor()
        self.performance = PerformanceTracker()
        self.user_sessions = {}
        self.user_settings = {}

# Initialize NOVAXA Core
core = EnhancedBot()

# Local Dev (optional) — start webhook if run directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=WEBHOOK_URL
    )

# Gunicorn entrypoint for Render
app = application
