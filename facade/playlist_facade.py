import models
import schemas
from facade.base_facade import BaseFacade
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class PlayList(BaseFacade):
    async def create_playlist(self, name: str, user_id: int) -> models.Playlist:
        db_playlist = models.Playlist(name=name, user_id=user_id)
        self.db.add(db_playlist)
        await self.db.commit()
        await self.db.refresh(db_playlist)
        return db_playlist

    async def add_song_to_playlist(self, song_id: int, playlist_id: int) -> schemas.PlaylistSong:
        song = await self.db.get(models.Song, song_id)
        playlist = await self.db.get(models.Playlist, playlist_id)

        if not song:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')

        if not playlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Playlist not found')

        existing_songs = await self.db.execute(
            select(models.PlaylistSong).filter_by(playlist_id=playlist_id, song_id=song_id)
        )

        if existing_songs.scalars().first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='You have already added this song')

        playlist_song = models.PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        self.db.add(playlist_song)
        await self.db.commit()
        await self.db.refresh(playlist_song)

        return schemas.PlaylistSong.from_orm(playlist_song)

    async def get_songs_in_playlist(self, playlist_id: int) -> list[schemas.PlaylistSong]:
        playlist_songs = await self.db.execute(
            select(models.PlaylistSong)
            .filter(models.PlaylistSong.playlist_id == playlist_id)
        )
        return [schemas.PlaylistSong.from_orm(song) for song in playlist_songs.scalars().all()]




playlist_facade = PlayList()