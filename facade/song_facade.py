import models
import schemas
from facade.base_facade import BaseFacade
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import func


class SongFacade(BaseFacade):

    async def create_song(self, song_data: schemas.SongCreate, file_path: str) -> models.Song:
        db_song = models.Song(title=song_data.title,
                              text=song_data.text,
                              album_id=song_data.album_id,
                              file_path=file_path
                              )
        self.db.add(db_song)
        await self.db.commit()
        await self.db.refresh(db_song)

        for genre_id in song_data.genres:
            genre = await self.db.get(models.Genre, genre_id)
            if genre:
                song_genre = models.SongGenreAssociation(song_id=db_song.id, genre_id=genre.id )
                self.db.add(song_genre)

        await self.db.commit()
        await self.db.refresh(db_song)

        return db_song

    async def get_song_by_genre(self, genre_id:int) -> list[schemas.Song]:
        genre = await self.db.get(models.Genre, genre_id)

        if not genre:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Genre not found')

        songs = await self.db.execute(
            select(models.Song,
            func.count(models.FavoriteSong.user_id).label('favorite_count')
            )
            .join(models.SongGenreAssociation)
            .outerjoin(models.FavoriteSong, models.Song.id == models.FavoriteSong.song_id)
            .filter(models.SongGenreAssociation.genre_id == genre_id)
            .group_by(models.Song.id)
            .order_by(func.count(models.FavoriteSong.user_id).desc())

            .limit(15)
        )

        songs = songs.scalars().all()
        return [schemas.Song(
            id=song.id,
            title=song.title,
            text=song.text,
            album_id=song.album_id,
            favorite_count=favorite_count
        ) for song, favorite_count in songs]



song_facade = SongFacade()