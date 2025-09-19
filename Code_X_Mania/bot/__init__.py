from pyrogram import Client
from ..vars import Var  # change to ..vars if inside a package

StreamBot = Client(
    name="filetolinkprobot",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
)
