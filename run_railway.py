"""
NEXTGEN AI — Cloud Production Runner for Railway / Render
Developer: Shohjahon Abdullayev
"""
import os
import sys
import asyncio
import logging
import multiprocessing
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("nextgen.runner")

def run_backend(port: int):
    logger.info("Starting NEXTGEN AI FastAPI Backend on port %d...", port)
    uvicorn.run("app.main:app", app_dir="backend", host="0.0.0.0", port=port, log_level="info")

def run_bot():
    logger.info("Starting NEXTGEN AI Telegram Demo Bot in background...")
    try:
        from bots.demo_bot import run as run_demo
        asyncio.run(run_demo())
    except Exception as e:
        logger.error("Telegram bot error: %s", e, exc_info=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mode = os.environ.get("SERVICE_TYPE", "both").lower()
    bot_token = os.environ.get("TELEGRAM_DEMO_BOT_TOKEN") or os.environ.get("BOT_TOKEN") or "9034127736:AAFdGFFoyD5HsqWHtOP9HQ07nd-wzy-zu7k"

    logger.info("=" * 60)
    logger.info("⚡ NEXTGEN AI — Cloud Production Service")
    logger.info("👨‍💻 Developer: Shohjahon Abdullayev")
    logger.info("⚙️ Mode: %s | Port: %d | Bot: @nextgenuzz_bot", mode, port)
    logger.info("=" * 60)

    if mode == "bot":
        from bots.demo_bot import run as run_demo
        asyncio.run(run_demo())
    elif mode == "backend":
        run_backend(port)
    else:
        # Default: "both"
        # Start bot as background process
        p_bot = multiprocessing.Process(target=run_bot, daemon=True)
        p_bot.start()
        logger.info("Demo Bot process started (PID: %s). Now launching FastAPI Backend...", p_bot.pid)
        # Start backend on main process
        run_backend(port)
