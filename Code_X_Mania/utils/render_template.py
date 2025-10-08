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

AUDIO_FORMATS = [
    'audio/mpeg',
    'audio/mp3',
    'audio/mp4',
    'audio/aac',
    'audio/ogg',
    'audio/opus',
    'audio/wav',
    'audio/x-wav',
    'audio/webm',
    'audio/flac',
    'audio/x-flac',
    'audio/x-m4a',
    'audio/x-ms-wma',
    'audio/amr',
    'audio/midi',
    'audio/x-midi',
]

VIDEO_FORMATS = [
    'video/mp4',
    'video/x-msvideo',
    'video/x-flv',
    'video/x-matroska',
    'video/webm',
    'video/ogg',
    'video/quicktime',
    'video/mpeg',
    'video/3gpp',
    'video/3gpp2',
    'video/h264',
    'video/h265',
    'video/x-ms-wmv',
    'video/x-ms-asf',
]

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
    audio_formats = AUDIO_FORMATS
    video_formats = VIDEO_FORMATS
    if mime_type.lower() in video_formats:
        async with aiofiles.open('Code_X_Mania/template/req.html') as r:
            heading = 'Watch {}'.format(file_name)
            tag = mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_name, src)
    elif mime_type.lower() in audio_formats:
        async with aiofiles.open('Code_X_Mania/template/req.html') as r:
            heading = 'Listen {}'.format(file_name)
            tag = mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_name, src)
    else:
        async with aiofiles.open('Code_X_Mania/template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(src) as u:
                    file_size = human_size(u.headers.get('Content-Type'))
                    html = (await r.read()) % (heading, file_name, src, file_size)
    return html
