import time, shutil, psutil
from utils_bot import *
from pyrogram import filters
from Code_X_Mania.bot import StreamBot
from Code_X_Mania import StartTime

@StreamBot.on_message(filters.private & filters.command("stats"))
async def status_command(bot, message):
    currentTime = readable_time(time.time() - StartTime)
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    botstats = (
    f"<b>Bot Uptime:</b> {currentTime}\n"
    f"<b>Total disk space:</b> {total}\n"
    f"<b>Used:</b> {used}  <b>Free:</b> {free}\n\n"
    f"📊Data Usage📊\n<b>Upload:</b> {sent}\n<b>Download:</b> {recv}\n\n"
    f"<b>CPU:</b> {cpuUsage}%  <b>RAM:</b> {memory}%  <b>Disk:</b> {disk}%")

    await message.reply_text(botstats, parse_mode="html")
