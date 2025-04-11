#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOVAXA_BOT v2.0 — Webhook Edition
Full Manus Spec with Modules and Webhook Mode for Render
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

# Internal Modules (Manus Spec)
from api import TelegramAPI, DataProcessor
from integration import ServiceIntegration, NotificationSystem
from monitor import SystemMonitor, PerformanceTracker

# Setup Logging
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("enhanced_bot")

# Get Bot Token
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment variables")

# Webhook URL (Render domain)
WEBHOOK_URL = "https://novaxa-v2-core.onrender.com/webhook"

# Init Application
application: Application = (
    ApplicationBuilder()
    .token(TOKEN)
    .webhook_url(WEBHOOK_URL)
    .build()
)

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Καλώς ήρθες στο NOVAXA_BOT v2.0 (Webhook Powered)!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Ενεργό και σε λειτουργία (Webhook).")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Enhanced Core Class (Manus Spec)
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

# Initialize core
core = EnhancedBot()

# Start Webhook Listener
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=WEBHOOK_URL
    )
