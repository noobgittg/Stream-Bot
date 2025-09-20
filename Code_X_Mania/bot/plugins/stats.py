import time
import shutil
import psutil
from pyrogram import filters
from Code_X_Mania.bot import StreamBot
from Code_X_Mania import StartTime
from utils_bot import get_readable_file_size
from Code_X_Mania.vars import Var

@StreamBot.on_message(filters.private & filters.command("stats") & filters.user(Var.OWNER_ID))
async def status_command(bot, message):
    # Uptime
    current_time = readable_time(time.time() - StartTime)

    # Disk usage
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)

    # Network usage
    net_io = psutil.net_io_counters()
    sent = get_readable_file_size(net_io.bytes_sent)
    recv = get_readable_file_size(net_io.bytes_recv)

    # System stats
    cpu_usage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Compose stats message
    botstats = (
        f"<b>Bot Uptime:</b> {current_time}\n"
        f"<b>Total disk space:</b> {total}\n"
        f"<b>Used:</b> {used}  <b>Free:</b> {free}\n\n"
        f"📊 Data Usage 📊\n"
        f"<b>Upload:</b> {sent}\n"
        f"<b>Download:</b> {recv}\n\n"
        f"<b>CPU:</b> {cpu_usage}%  <b>RAM:</b> {memory}%  <b>Disk:</b> {disk}%"
    )

    await message.reply_text(botstats, parse_mode=enums.ParseMode.HTML)
