import os
import asyncio
from asyncio import TimeoutError
from Code_X_Mania.bot import StreamBot
from Code_X_Mania.utils.database import Database
from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


# ✅ Private handler: direct file receive (no login)
@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))
async def private_receive_handler(c: Client, m: Message):
    try:
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id)
            await c.send_message(
                Var.BIN_CHANNEL,
                f"New User Joined:\n\nName: [{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
            )

        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await c.send_message(
                        chat_id=m.chat.id,
                        text="Sorry, you are banned from using me.\n\nContact developer @adarshgoelz",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await c.send_message(
                    chat_id=m.chat.id,
                    text=f"Join updates channel @{Var.UPDATES_CHANNEL} to use me."
                )
                return
            except Exception as e:
                await m.reply_text(str(e))
                await c.send_message(
                    chat_id=m.chat.id,
                    text="Something went wrong. Contact my boss @adarshgoelz",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return

        # 📂 File Info
        file_size = None
        if m.video:
            file_size = f"{humanbytes(m.video.file_size)}"
            file_name = m.video.file_name
        elif m.document:
            file_size = f"{humanbytes(m.document.file_size)}"
            file_name = m.document.file_name
        elif m.audio:
            file_size = f"{humanbytes(m.audio.file_size)}"
            file_name = m.audio.file_name
        elif m.photo:
            file_size = f"{humanbytes(m.photo.file_size)}"
            file_name = "Photo"

        # 🔗 Generate Links
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = Var.URL + "watch/" + str(log_msg.message_id)
        online_link = Var.URL + "download/" + str(log_msg.message_id)

        msg_text = f"""
<i><u>Your Link Generated!</u></i>

<b>📂 File Name:</b> <i>{file_name}</i>
<b>📦 File Size:</b> <i>{file_size}</i>
<b>📥 Download:</b> <i>{online_link}</i>
<b>🖥 Watch:</b> <i>{stream_link}</i>

<b>🚸 Note: Link won't expire till I delete.</b>
"""

        await log_msg.reply_text(
            text=f"Requested by: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nUser ID: `{m.from_user.id}`\nStream Link: {stream_link}",
            disable_web_page_preview=True,
            parse_mode="Markdown",
            quote=True
        )
        await m.reply_text(
            text=msg_text,
            parse_mode="HTML",
            quote=True,
            disable_web_page_preview=True
        )

    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"Got FloodWait of {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\nUser ID: `{str(m.from_user.id)}`",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )


# ✅ Channel Handler (no password check)
@StreamBot.on_message(filters.channel & (filters.document | filters.video | filters.photo) & filters.forwarded)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = Var.URL + "watch/" + str(log_msg.message_id)
        online_link = Var.URL + "download/" + str(log_msg.message_id)

        await log_msg.reply_text(
            text=f"Channel Name: `{broadcast.chat.title}`\nChannel ID: `{broadcast.chat.id}`\nRequest URL: {stream_link}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.send_message(
            chat_id=broadcast.chat.id,
            text=f"Generated Links:\n\nWatch: {stream_link}\nDownload: {online_link}"
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"Got FloodWait of {str(w.x)}s from {broadcast.chat.title}\n\nChannel ID: `{str(broadcast.chat.id)}`",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    except Exception as e:
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"Error: `{e}`",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
        print(f"Can't edit broadcast message! Error: {e}")
