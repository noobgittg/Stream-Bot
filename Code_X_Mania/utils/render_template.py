from Code_X_Mania.vars import Var
from Code_X_Mania.bot import StreamBot
from Code_X_Mania.utils.custom_dl import TGCustomYield
from Code_X_Mania.utils.file_size import human_size
import urllib.parse
import secrets
import mimetypes
import aiofiles
import logging
import aiohttp

async def fetch_properties(message_id):
    media_msg = await StreamBot.get_messages(Var.BIN_CHANNEL, message_id)
    file_properties = await TGCustomYield().generate_file_properties(media_msg)
    file_name = file_properties.file_name if file_properties.file_name \
        else f"{secrets.token_hex(2)}.jpeg"
    mime_type = file_properties.mime_type if file_properties.mime_type \
        else f"{mimetypes.guess_type(file_name)}"
    return file_name, mime_type

async def render_page(message_id):
    file_name, mime_type = await fetch_properties(message_id)
    src = urllib.parse.urljoin(Var.URL, str(message_id))

    audio_formats = [
        'audio/mpeg', 'audio/mp4', 'audio/x-mpegurl',
        'audio/vnd.wav', 'audio/ogg', 'audio/webm', 'audio/x-wav'
    ]

    video_formats = [
        'video/mp4', 'video/avi', 'video/ogg', 'video/h264',
        'video/h265', 'video/x-matroska', 'video/webm'
    ]

    # Default heading
    heading = f"File: {file_name}"

    # Handle video and audio
    if mime_type.lower() in video_formats:
        async with aiofiles.open('Code_X_Mania/template/req.html', mode='r') as r:
            heading = f"Watch {file_name}"
            tag = 'video'
            html_template = await r.read()
            html = html_template.replace('tag', tag) % (heading, file_name, src)

    elif mime_type.lower() in audio_formats:
        async with aiofiles.open('Code_X_Mania/template/req.html', mode='r') as r:
            heading = f"Listen {file_name}"
            tag = 'audio'
            html_template = await r.read()
            html = html_template.replace('tag', tag) % (heading, file_name, src)

    # Handle other files (download link)
    else:
        async with aiofiles.open('Code_X_Mania/template/dl.html', mode='r') as r:
            async with aiohttp.ClientSession() as session:
                async with session.head(src) as response:
                    content_length = response.headers.get('Content-Length')
                    file_size = human_size(int(content_length)) if content_length else "Unknown"
            heading = f"Download {file_name}"
            html_template = await r.read()
            html = html_template % (heading, file_name, src, file_size)

    return html
