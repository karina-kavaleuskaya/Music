from fastapi import File, UploadFile, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from facade.facade import FILE_MANAGER
import models
import schemas
import os
import logging


class SongManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_song(self, song_id: int) -> schemas.Song:
        song = await self.db.get(models.Song, song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        return schemas.Song.from_orm(song)

    async def download_file(self, song_id: int) -> Response:
        song = await self.db.get(models.Song, song_id)
        if not song:
            logging.error(f"Song with id {song_id} not found")
            raise HTTPException(status_code=404, detail="Song not found")

        file_path = os.path.join(FILE_MANAGER.base_directory, song.file_path.lstrip('static/songs/'))
        logging.info(f"Trying to get file at path: {file_path}")
        try:
            file_data = await FILE_MANAGER.get_file(file_path)
        except HTTPException as e:
            if e.status_code == 404:
                logging.error(f"File not found at path: {file_path}")
                raise HTTPException(status_code=404, detail="File not found")
            else:
                logging.error(f"Error getting file: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error getting file: {str(e)}")

        return Response(
            content=file_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={song.title}"
            }
        )