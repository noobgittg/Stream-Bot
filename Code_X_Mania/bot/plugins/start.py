from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
import logging
logger = logging.getLogger(__name__)

from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

@StreamBot.on_message(filters.command("maintainers") & filters.private)
async def maintainers_handler(b, m):
    try:
        await b.send_message(chat_id=m.chat.id, text="HELLO", quote=True)
    except Exception:
        await b.send_message(
            chat_id=m.chat.id,
            text="I am Coded By Adarsh Goel and Sponsored by [Gopal Naik](https://t.me/Movie_leecher)",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Developer💻", url="https://t.me/adarsh_goel")]]
            ),
            parse_mode="markdown",
            disable_web_page_preview=True
        )


@StreamBot.on_message(filters.command("follow") & filters.private)
async def follow_handler(b, m):
    try:
        await b.send_message(chat_id=m.chat.id, text="HELLO", quote=True)
    except Exception:
        await b.send_message(
            chat_id=m.chat.id,
            text="<B>HERE'S THE FOLLOW LINK</B>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("FOLLOW ME", url="https://GITHUB.COM/CODE-X-MANIA")]]
            ),
            parse_mode="HTML",
            disable_web_page_preview=True
        )


@StreamBot.on_message(filters.command("start") & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
        )

    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                return await b.send_message(
                    chat_id=m.chat.id,
                    text="__You are banned from using me! Contact @codexmaniabot__",
                    parse_mode="markdown"
                )
        except UserNotParticipant:
            return await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://i.ibb.co/NKXgXD4/vlmnwosn-0.png",
                caption="<i>Join the updates channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]
                ),
                parse_mode="HTML"
            )
        except Exception:
            return await b.send_message(
                chat_id=m.chat.id,
                text="<i>Something went wrong!</i>",
                parse_mode="HTML"
            )

    await StreamBot.send_photo(
        chat_id=m.chat.id,
        photo="https://user-images.githubusercontent.com/88939380/137127129-a86fc939-2931-4c66-b6f6-b57711a9eab7.png",
        caption="Hi! I am Telegram File to Link Generator Bot with Channel support.\n\nSend me any file and get direct download & stream links!",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Help 📚", callback_data="help")],
                [InlineKeyboardButton("Maintainers 😎", callback_data="maintainers")],
                [InlineKeyboardButton("Follow ❤️", callback_data="follow")]
            ]
        )
    )

@StreamBot.on_message(filters.command("help") & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ **\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) started your bot!"
        )

    await message.reply_text(
        text="""<b>Send me any file or video, I will give you streamable & download links.</b>\n
<b>I also support Channels: Add me to your Channel, send media & get links!</b>\n
<b>Commands:</b>
/start - Start the bot
/help - Show this help
/follow - Follow my GitHub
/maintainers - Show bot maintainers""",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💁‍♂️ DEV", url="https://t.me/codexmania")],
                [InlineKeyboardButton("💥 FOLLOW", url="https://GitHub.com/code-x-mania")]
            ]
        )
    )
