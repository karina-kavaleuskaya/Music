import models
import schemas
from facade.base_facade import BaseFacade
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class FavouriteSongFacade(BaseFacade):
    async def add_favourite_song(self, song_id: int, user_id: int) -> schemas.FavouriteSong:
        song = await self.db.get(models.Song, song_id)

        if not song:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')

        existing_favourite = await self.db.execute(
            select(models.FavoriteSong).filter_by(user_id=user_id, song_id=song_id)
        )

        if existing_favourite.scalars().first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='You have already added this song')

        favourite_song = models.FavoriteSong(user_id=user_id, song_id=song_id)
        self.db.add(favourite_song)
        await self.db.commit()
        await self.db.refresh(favourite_song)

        return schemas.FavouriteSong.from_orm(favourite_song)


    async def get_favourite_song(self, user_id:int) -> list[schemas.Song]:
        favourite_songs = await self.db.execute(
            select(models.FavoriteSong).filter_by(user_id=user_id).options(selectinload(models.FavoriteSong.song))
        )
        favourite_songs = favourite_songs.scalars().all()

        return [schemas.Song.from_orm(favourite_song.song) for favourite_song in favourite_songs]


favourite_song_facade = FavouriteSongFacade()