import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, APIRouter
from async_db import get_db
from users import get_current_user
from facade.favourite_song_facade import favourite_song_facade
from facade.song_facade import song_facade


router = APIRouter(
    prefix='/api',
    tags=['API']
)


@router.post('/favourites/', response_model=schemas.FavouriteSong)
async def add_favourite_song(
        song_data: schemas.FavouriteSongCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    favourite_song = await favourite_song_facade.add_favourite_song(
        song_id=song_data.song_id, user_id=current_user.id
    )

    return favourite_song


@router.get('/favourites/', response_model=list[schemas.Song])
async def get_user_favourite(
        current_user: models.User = Depends(get_current_user)
):
    favourite_songs = await favourite_song_facade.get_favourite_song(user_id=current_user.id)
    return favourite_songs


@router.get('/songs/genre/{genre_id}', response_model=list[schemas.Song])
async def get_songs_by_genre(
        genre_id: int,
        current_user: models.User = Depends(get_current_user)
):
    songs = await song_facade.get_song_by_genre(genre_id)
    return songs