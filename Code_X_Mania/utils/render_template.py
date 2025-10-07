import urllib.parse
import secrets
import mimetypes
import aiofiles
import logging
import aiohttp
from Code_X_Mania.vars import Var
from Code_X_Mania.bot import StreamBot
from Code_X_Mania.utils.custom_dl import TGCustomYield
from Code_X_Mania.utils.file_size import human_size
from pyrogram import enums

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def fetch_properties(message_id):
    try:
        media_msg = await StreamBot.get_messages(Var.BIN_CHANNEL, message_id)
        if not media_msg:
            logger.error(f"Message not found for ID {message_id}")
            return None, None

        file_props = await TGCustomYield().generate_file_properties(media_msg)
        file_name = file_props.file_name or f"{secrets.token_hex(2)}.bin"
        mime_type = file_props.mime_type or mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        logger.info(f"Fetched file: {file_name} | MIME: {mime_type}")
        return file_name, mime_type

    except Exception as e:
        logger.exception(f"Error fetching properties for message {message_id}: {e}")
        return None, None


async def render_page(message_id):
    try:
        file_name, mime_type = await fetch_properties(message_id)
        if not file_name or not mime_type:
            logger.warning("Invalid file properties.")
            return "<h3>Error: Unable to retrieve file information.</h3>"

        src = urllib.parse.urljoin(Var.URL, str(message_id))
        mime_lower = mime_type.lower()

        audio_formats = [
            'audio/mpeg', 'audio/mp4', 'audio/x-mpegurl', 'audio/vnd.wav',
            'audio/ogg', 'audio/webm', 'audio/x-wav'
        ]
        video_formats = [
            'video/mp4', 'video/avi', 'video/ogg', 'video/h264',
            'video/h265', 'video/x-matroska', 'video/webm'
        ]

        heading = file_name
        html = ""

        if mime_lower in video_formats:
            async with aiofiles.open('Code_X_Mania/template/req.html', mode='r') as f:
                tag = "video"
                html = (await f.read()).replace('tag', tag) % (f"Watch {file_name}", file_name, src)
            logger.info(f"Rendering video page for {file_name}")

        elif mime_lower in audio_formats:
            async with aiofiles.open('Code_X_Mania/template/req.html', mode='r') as f:
                tag = "audio"
                html = (await f.read()).replace('tag', tag) % (f"Listen {file_name}", file_name, src)
            logger.info(f"Rendering audio page for {file_name}")

        else:
            async with aiofiles.open('Code_X_Mania/template/dl.html', mode='r') as f:
                async with aiohttp.ClientSession() as session:
                    async with session.head(src) as response:
                        size_header = response.headers.get('Content-Length')
                        file_size = human_size(size_header) if size_header else "Unknown Size"
                html = (await f.read()) % (f"Download {file_name}", file_name, src, file_size)
            logger.info(f"Rendering document/download page for {file_name}")

        return html

    except Exception as e:
        logger.exception(f"Error rendering page for message {message_id}: {e}")
        return "<h3>Internal Error: Unable to load file preview.</h3>"
