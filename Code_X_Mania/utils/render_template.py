import aiofiles
import aiohttp
import urllib.parse
import secrets
import mimetypes
import logging

from Code_X_Mania.vars import Var
from Code_X_Mania.bot import StreamBot
from Code_X_Mania.utils.custom_dl import TGCustomYield
from Code_X_Mania.utils.file_size import human_size

AUDIO_FORMATS = {
    'audio/mpeg', 'audio/mp3', 'audio/mp4', 'audio/aac', 'audio/ogg', 'audio/opus',
    'audio/wav', 'audio/x-wav', 'audio/webm', 'audio/flac', 'audio/x-flac',
    'audio/x-m4a', 'audio/x-ms-wma', 'audio/amr', 'audio/midi', 'audio/x-midi',
}

VIDEO_FORMATS = {
    'video/mp4', 'video/x-msvideo', 'video/x-flv', 'video/x-matroska',
    'video/webm', 'video/ogg', 'video/quicktime', 'video/mpeg', 'video/3gpp',
    'video/3gpp2', 'video/h264', 'video/h265', 'video/x-ms-wmv', 'video/x-ms-asf',
}


async def fetch_properties(message_id: int):
    try:
        media_msg = await StreamBot.get_messages(Var.BIN_CHANNEL, message_id)
        file_props = await TGCustomYield().generate_file_properties(media_msg)

        file_name = file_props.file_name or f"{secrets.token_hex(2)}.bin"
        mime_type = file_props.mime_type

        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file_name)
            mime_type = mime_type or "application/octet-stream"

        return file_name, mime_type

    except Exception as e:
        logging.error(f"Error fetching file properties: {e}")
        return f"{secrets.token_hex(2)}.bin", "application/octet-stream"


async def render_page(message_id: int):
    file_name, mime_type = await fetch_properties(message_id)
    src = urllib.parse.urljoin(Var.URL, str(message_id))
    mime_main = mime_type.split('/')[0].lower()

    try:
        if mime_type.lower() in VIDEO_FORMATS or mime_type.lower() in AUDIO_FORMATS:
            async with aiofiles.open('Code_X_Mania/template/req.html', mode='r') as r:
                template = await r.read()
                heading = f"{'Watch' if mime_main == 'video' else 'Listen'} {file_name}"
                html = template.replace('tag', mime_main) % (heading, file_name, src)
        else:
            async with aiofiles.open('Code_X_Mania/template/dl.html', mode='r') as r:
                template = await r.read()
                async with aiohttp.ClientSession() as session:
                    async with session.head(src) as response:
                        size_header = response.headers.get('Content-Length')
                        file_size = human_size(size_header) if size_header else "Unknown size"
                heading = f"Download {file_name}"
                html = template % (heading, file_name, src, file_size)

        return html

    except Exception as e:
        logging.error(f"Error rendering page: {e}")
        return f"<h3>Error loading {file_name}</h3><p>{e}</p>"
