import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
from Code_X_Mania.utils.database import Database

logger = logging.getLogger(__name__)
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command("start") & filters.private)
async def start_command(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:**\n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
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
            return await b.send_photo(
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

    await b.send_photo(
        chat_id=m.chat.id,
        photo="https://envs.sh/dp1.jpg",
        caption=(
            f'<b>ʜᴇʟʟᴏ <a href="tg://user?id={m.from_user.id}">{m.from_user.first_name}</a>...⚡\n\n'
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
async def help_command(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:**\n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
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
            return await b.send_photo(
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

    await b.send_photo(
        chat_id=m.chat.id,
        photo="https://envs.sh/dp1.jpg",
        caption=(
            "<b>┣⪼ Sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ/ᴠɪᴅᴇᴏ, ᴛʜᴇɴ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ.\n"
            "┣⪼ Tʜɪs ʟɪɴᴋ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴏʀ sᴛʀᴇᴀᴍ ᴜsɪɴɢ ᴇxᴛᴇʀɴᴀʟ ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀs.\n"
            "┣⪼ Fᴏʀ sᴛʀᴇᴀᴍɪɴɢ, ᴄᴏᴘʏ ᴛʜᴇ ʟɪɴᴋ ᴀɴᴅ ᴘᴀsᴛᴇ ɪɴ ʏᴏᴜʀ ᴠɪᴅᴇᴏ ᴘʟᴀʏᴇʀ.\n"
            "┣⪼ Tʜɪs ʙᴏᴛ ᴀʟsᴏ sᴜᴘᴘᴏʀᴛs ᴄʜᴀɴɴᴇʟs. Aᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ʀᴇᴀʟᴛɪᴍᴇ ʟɪɴᴋs ғᴏʀ ғɪʟᴇs/ᴠɪᴅᴇᴏs.\n"
            "┣⪼ Fᴏʀ ᴍᴏʀᴇ ɪɴғᴏ :- /about\n"
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


@StreamBot.on_message(filters.command("about") & filters.private)
async def about_command(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:**\n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) started your bot!"
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
            return await b.send_photo(
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

    await b.send_photo(
        chat_id=m.chat.id,
        photo="https://envs.sh/dp1.jpg",
        caption=(
            "<b>sᴏᴍᴇ ʜɪᴅᴅᴇɴ ᴅᴇᴛᴀɪʟs😜\n\n"
            "╭━━━━━━━〔ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ〕\n"
            "┃\n"
            "┣⪼ʙᴏᴛ ɴᴀᴍᴇ : ғɪʟᴇ ᴛᴏ ʟɪɴᴋ\n"
            "┣⪼ᴜᴘᴅᴀᴛᴇᴢ : <a href=https://t.me/mallumovieworldmain1>𝙈𝙈𝙒 𝘽𝙊𝙏𝙕</a>\n"
            "┣⪼sᴜᴘᴘᴏʀᴛ : <a href=https://t.me/mallumovieworldmain1>𝚂𝚄𝙿𝙿𝙾𝚁𝚃</a>\n"
            "┣⪼sᴇʀᴠᴇʀ : ʜᴇʀᴜᴋᴏ\n"
            "┣⪼ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ\n"
            "┣⪼ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ 3.10\n"
            "┣⪼ʏᴏᴜᴛᴜʙᴇ : <a href=https://t.me/mallumovieworldmain1>𝙈𝙈𝙒 𝘽𝙊𝙏𝙕</a>\n"
            "┃\n"
            "╰━━━━━━━〔ᴘʟᴇᴀsʀ sᴜᴘᴘᴏʀᴛ〕</b>"
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
