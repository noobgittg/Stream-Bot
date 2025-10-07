import math
from typing import Union, AsyncGenerator, List
from pyrogram.types import Message
from pyrogram import Client, utils, raw, enums
from pyrogram.session import Session, Auth
from pyrogram.errors import AuthBytesInvalid
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from ..bot import StreamBot


async def chunk_size(length: int) -> int:
    return 2 ** max(min(math.ceil(math.log2(length / 1024)), 10), 2) * 1024


async def offset_fix(offset: int, chunksize: int) -> int:
    return offset - (offset % chunksize)


class TGCustomYield:
    def __init__(self):
        self.main_bot = StreamBot

    @staticmethod
    async def generate_file_properties(msg: Message) -> FileId:
        supported_types = (
            enums.MessageMediaType.VIDEO,
            enums.MessageMediaType.AUDIO,
            enums.MessageMediaType.DOCUMENT,
            enums.MessageMediaType.PHOTO,
            enums.MessageMediaType.VOICE,
            enums.MessageMediaType.VIDEO_NOTE,
            enums.MessageMediaType.STICKER,
            enums.MessageMediaType.ANIMATION
        )

        if not isinstance(msg, Message):
            raise ValueError("Invalid message type")

        media = None
        for mtype in supported_types:
            media = getattr(msg, mtype.name.lower(), None)
            if media:
                break

        if not media:
            raise ValueError("This message doesn't contain any supported downloadable media")

        file_id_obj = FileId.decode(media.file_id)
        file_id_obj.file_size = getattr(media, "file_size", 0)
        file_id_obj.mime_type = getattr(media, "mime_type", "")
        file_id_obj.file_name = getattr(media, "file_name", "")

        return file_id_obj

    async def generate_media_session(self, client: Client, msg: Message) -> Session:
        data = await self.generate_file_properties(msg)
        media_session = client.media_sessions.get(data.dc_id)

        if media_session:
            return media_session

        if data.dc_id != await client.storage.dc_id():
            auth = await Auth(client, data.dc_id, await client.storage.test_mode()).create()
        else:
            auth = await client.storage.auth_key()

        media_session = Session(
            client,
            data.dc_id,
            auth,
            await client.storage.test_mode(),
            is_media=True
        )
        await media_session.start()

        if data.dc_id != await client.storage.dc_id():
            for _ in range(3):
                exported_auth = await client.invoke(raw.functions.auth.ExportAuthorization(dc_id=data.dc_id))
                try:
                    await media_session.invoke(
                        raw.functions.auth.ImportAuthorization(id=exported_auth.id, bytes=exported_auth.bytes)
                    )
                    break
                except AuthBytesInvalid:
                    continue
            else:
                await media_session.stop()
                raise AuthBytesInvalid

        client.media_sessions[data.dc_id] = media_session
        return media_session

    @staticmethod
    async def get_location(file_id: FileId) -> raw.base.InputFileLocation:
        if file_id.file_type == FileType.CHAT_PHOTO:
            if file_id.chat_id > 0:
                peer = raw.types.InputPeerUser(user_id=file_id.chat_id, access_hash=file_id.chat_access_hash)
            elif file_id.chat_access_hash == 0:
                peer = raw.types.InputPeerChat(chat_id=-file_id.chat_id)
            else:
                peer = raw.types.InputPeerChannel(
                    channel_id=utils.get_channel_id(file_id.chat_id),
                    access_hash=file_id.chat_access_hash
                )
            return raw.types.InputPeerPhotoFileLocation(
                peer=peer,
                volume_id=file_id.volume_id,
                local_id=file_id.local_id,
                big=file_id.thumbnail_source == ThumbnailSource.CHAT_PHOTO_BIG
            )

        if file_id.file_type == FileType.PHOTO:
            return raw.types.InputPhotoFileLocation(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
                thumb_size=file_id.thumbnail_size
            )

        return raw.types.InputDocumentFileLocation(
            id=file_id.media_id,
            access_hash=file_id.access_hash,
            file_reference=file_id.file_reference,
            thumb_size=file_id.thumbnail_size
        )

    async def yield_file(
        self,
        media_msg: Message,
        offset: int,
        first_part_cut: int,
        last_part_cut: int,
        part_count: int,
        chunk_size: int
    ) -> AsyncGenerator[bytes, None]:
        client = self.main_bot
        data = await self.generate_file_properties(media_msg)
        media_session = await self.generate_media_session(client, media_msg)
        location = await self.get_location(data)

        for current_part in range(1, part_count + 1):
            r = await media_session.invoke(
                raw.functions.upload.GetFile(location=location, offset=offset, limit=chunk_size)
            )
            if not isinstance(r, raw.types.upload.File) or not r.bytes:
                break

            chunk = r.bytes
            if part_count == 1:
                yield chunk[first_part_cut:last_part_cut]
                break
            elif current_part == 1:
                yield chunk[first_part_cut:]
            elif current_part < part_count:
                yield chunk
            else:
                yield chunk[:last_part_cut]

            offset += chunk_size

    async def download_as_bytesio(self, media_msg: Message) -> List[bytes]:
        client = self.main_bot
        data = await self.generate_file_properties(media_msg)
        media_session = await self.generate_media_session(client, media_msg)
        location = await self.get_location(data)

        limit = 1024 * 1024
        offset = 0
        result = []

        while True:
            r = await media_session.invoke(
                raw.functions.upload.GetFile(location=location, offset=offset, limit=limit)
            )
            if not isinstance(r, raw.types.upload.File) or not r.bytes:
                break

            result.append(r.bytes)
            offset += limit

        return result
