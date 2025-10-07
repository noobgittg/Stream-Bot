import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import idle
from aiohttp import web
from apscheduler.schedulers.background import BackgroundScheduler

from .bot import StreamBot
from .vars import Var
from .server import web_server
from .utils.keepalive import ping_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Code_X_Mania")
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

PLUGINS_PATH = "Code_X_Mania/bot/plugins/*.py"
plugin_files = glob.glob(PLUGINS_PATH)

StreamBot.start()

loop = asyncio.get_event_loop()

async def start_services():
    logger.info("Initializing Telegram Bot...")

    # Import plugins dynamically
    logger.info("Importing plugins...")
    for path in plugin_files:
        plugin_path = Path(path)
        plugin_name = plugin_path.stem
        try:
            spec = importlib.util.spec_from_file_location(
                f".plugins.{plugin_name}", plugin_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[f"Code_X_Mania.bot.plugins.{plugin_name}"] = module
            logger.info(f"✅ Plugin imported: {plugin_name}")
        except Exception as e:
            logger.error(f"❌ Failed to import plugin {plugin_name}: {e}", exc_info=True)

    # Setup Keep Alive if on Heroku
    if Var.ON_HEROKU:
        logger.info("Starting Keep Alive Scheduler (Heroku Mode)")
        scheduler = BackgroundScheduler()
        scheduler.add_job(ping_server, "interval", seconds=1200)
        scheduler.start()

    # Initialize web server
    logger.info("Starting Web Server...")
    runner = web.AppRunner(await web_server())
    await runner.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    await web.TCPSite(runner, bind_address, Var.PORT).start()
    logger.info(f"Web Server running on {bind_address}:{Var.PORT}")

    # Bot details
    bot_user = await StreamBot.get_me()
    logger.info("--------------------------- SERVICE STARTED ---------------------------")
    logger.info(f"Bot Name      : {bot_user.first_name}")
    logger.info(f"Owner         : {Var.OWNER_USERNAME}")
    logger.info(f"Server        : {bind_address}:{Var.PORT}")
    if Var.ON_HEROKU:
        logger.info(f"App (Heroku)  : {Var.FQDN}")
    logger.info("-----------------------------------------------------------------------")

    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logger.info("Service Stopped by User")
    except Exception as e:
        logger.exception(f"Critical error occurred: {e}")
    finally:
        loop.close()
        logger.info("Event loop closed. Shutdown complete.")
