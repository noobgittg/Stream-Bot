from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
import logging
logger = logging.getLogger(__name__)

from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.utils.database import Database
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums

@Client.on_message(filters.command(['help','rule','rules']))
async def ai_generate_private(client, message):
    buttons = [[
            InlineKeyboardButton('⚙️ 𝘽𝙤𝙩 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚙️', url='https://t.me/mallumovieworldmain3'),
            ],[
            InlineKeyboardButton(' ⚓ 𝙊𝙏𝙏 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚓ ', url='https://t.me/+bG-xSQIgDBphODhl'),
            ],[
            InlineKeyboardButton('💻 𝙊𝙏𝙏 𝙐𝙥𝙙𝙖𝙩𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 💻', url='https://t.me/mallumovieworldmain1')
        ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        text="""<b><blockquote>❗️How to Search Movies Here❓
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
1. Just Send Movie Name and Movie Released Year Correctly.
<blockquote>(Check Google for Correct Movie Spelling and Movie Released Year)</blockquote>

Examples: -
Oppam 2016
Baahubali 2015 1080p
<blockquote>(For Getting only 1080p Quality Files)</blockquote>
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Baahubali 2015 Malayalam
Baahubali 2015 Tamil
<blockquote>(For Dubbed Movie Files)</blockquote>
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
❗️On Android, Better Use VLC Media Player For Watch Movie's.
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</b>""",
        reply_markup=reply_markup
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
                    parse_mode=enums.ParseMode.HTML
                )
        except UserNotParticipant:
            return await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://i.ibb.co/NKXgXD4/vlmnwosn-0.png",
                caption="<i>Join the updates channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]
                ),
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            return await b.send_message(
                chat_id=m.chat.id,
                text="<i>Something went wrong!</i>",
                parse_mode=enums.ParseMode.HTML,
            )

    await StreamBot.send_photo(
        chat_id=m.chat.id,
        photo="https://user-images.githubusercontent.com/88939380/137127129-a86fc939-2931-4c66-b6f6-b57711a9eab7.png",
        caption="Hi! I am Telegram File to Link Generator Bot with Channel support.\n\nSend me any file and get direct download & stream links!",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('⚙️ 𝘽𝙤𝙩 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚙️', url='https://t.me/mallumovieworldmain3'),
            ],[
            InlineKeyboardButton(' ⚓ 𝙊𝙏𝙏 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚓ ', url='https://t.me/+bG-xSQIgDBphODhl'),
            ],[
            InlineKeyboardButton('💻 𝙊𝙏𝙏 𝙐𝙥𝙙𝙖𝙩𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 💻', url='https://t.me/mallumovieworldmain1')
        ]]
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
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('⚙️ 𝘽𝙤𝙩 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚙️', url='https://t.me/mallumovieworldmain3'),
            ],[
            InlineKeyboardButton(' ⚓ 𝙊𝙏𝙏 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚓ ', url='https://t.me/+bG-xSQIgDBphODhl'),
            ],[
            InlineKeyboardButton('💻 𝙊𝙏𝙏 𝙐𝙥𝙙𝙖𝙩𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 💻', url='https://t.me/mallumovieworldmain1')
        ]]
        )
    )
