from Code_X_Mania.bot import StreamBot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LIST_MSG = """𝙃𝙞! {} ✨  
𝙃𝙚𝙧𝙚’𝙨 𝙖 𝙡𝙞𝙨𝙩 𝙤𝙛 𝙖𝙡𝙡 𝙢𝙮 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨 ⬇️  

1. `/start ⚡️`  
2. `/help 📚`  
5. `/ping 📡`  
6. `/status 📊`  
8. `/maintainers 😎`  
"""

@StreamBot.on_message(filters.command("list"))
def _list(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text=LIST_MSG.format(message.from_user.mention),
        reply_to_message_id=message.message_id,
        parse_mode="markdown"
    )
