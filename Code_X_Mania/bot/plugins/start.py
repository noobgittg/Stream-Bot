import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.utils.database import Database

logger = logging.getLogger(__name__)
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


# /start command
@StreamBot.on_message(filters.command("start") & filters.private)
async def start(b, m):
    # Add new user to DB if not already exists
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:**\n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
        )

    await b.send_photo(
        chat_id=m.chat.id,
        photo="https://envs.sh/dp1.jpg",
        caption=(
            "<b>ʜᴇʟʟᴏ...⚡\n\n"
            "ɪ ᴀᴍ ᴀ sɪᴍᴘʟᴇ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ/ᴠɪᴅᴇᴏ ᴛᴏ ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ ᴀɴᴅ sᴛʀᴇᴀᴍ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ.\n\n"
            "ᴜsᴇ /help ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs.\n\n"
            "sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴠɪᴅᴇᴏ / ғɪʟᴇ ᴛᴏ sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ...</b>"
        ),
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('⚙️ 𝘽𝙤𝙩 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚙️', url='https://t.me/mallumovieworldmain3')],
                [InlineKeyboardButton('⚓ 𝙊𝙏𝙏 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚓', url='https://t.me/+bG-xSQIgDBphODhl')],
                [InlineKeyboardButton('💻 𝙊𝙏𝙏 𝙐𝙥𝙙𝙖𝙩𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 💻', url='https://t.me/mallumovieworldmain1')]
            ]
        )
    )


@StreamBot.on_message(filters.command("help") & filters.private)
async def start(b, m):
    # Add new user to DB if not already exists
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:**\n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
        )

    await b.send_photo(
        chat_id=m.chat.id,
        photo="https://envs.sh/dp1.jpg",
        caption=(
            "<b>┣⪼ Sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ/ᴠɪᴅᴇᴏ, ᴛʜᴇɴ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ.\n\n"
            "┣⪼ Tʜɪs ʟɪɴᴋ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴏʀ sᴛʀᴇᴀᴍ ᴜsɪɴɢ ᴇxᴛᴇʀɴᴀʟ ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀs.\n\n"
            "┣⪼ Fᴏʀ sᴛʀᴇᴀᴍɪɴɢ, ᴄᴏᴘʏ ᴛʜᴇ ʟɪɴᴋ ᴀɴᴅ ᴘᴀsᴛᴇ ɪᴛ ɪɴ ʏᴏᴜʀ ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀ.\n\n"
            "┣⪼ Tʜɪs ʙᴏᴛ ᴀʟsᴏ sᴜᴘᴘᴏʀᴛs ᴄʜᴀɴɴᴇʟs. Aᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ʀᴇᴀʟᴛɪᴍᴇ ʟɪɴᴋs ғᴏʀ ғɪʟᴇs/ᴠɪᴅᴇᴏs.\n\n"
            "┣⪼ Fᴏʀ ᴍᴏʀᴇ ɪɴғᴏ :- /about\n\n"
            "ᴘʟᴇᴀsᴇ sʜᴀʀᴇ ᴀɴᴅ sᴜʙsᴄʀɪʙᴇ </b>"
        ),
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('⚙️ 𝘽𝙤𝙩 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚙️', url='https://t.me/mallumovieworldmain3')],
                [InlineKeyboardButton('⚓ 𝙊𝙏𝙏 𝙈𝙤𝙫𝙞𝙚 𝙂𝙧𝙤𝙪𝙥 ⚓', url='https://t.me/+bG-xSQIgDBphODhl')],
                [InlineKeyboardButton('💻 𝙊𝙏𝙏 𝙐𝙥𝙙𝙖𝙩𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 💻', url='https://t.me/mallumovieworldmain1')]
            ]
        )
    )


