import models
import schemas
import os
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, APIRouter, Response
from async_db import get_db
from users import get_current_user
from facade.favourite_song_facade import favourite_song_facade
from facade.song_facade import song_facade
from facade.playlist_facade import playlist_facade
from facade.facade import FILE_MANAGER

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


@router.post('/playlist/', response_model=schemas.Playlist)
async def create_playlist(
        name: str,
        current_user: models.User = Depends(get_current_user)
):
    db_playlist = await playlist_facade.create_playlist(name, user_id=current_user.id)

    return db_playlist


@router.post('/playlist/add-songs/', response_model=schemas.PlaylistSong)
async def add_playlist_song(
        payload: schemas.PlaylistSongCreate,
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    playlist_song = await playlist_facade.add_song_to_playlist(
        song_id=payload.song_id, playlist_id=payload.playlist_id
    )

    return playlist_song


@router.get('/playlist/{playlist_id}/songs/', response_model=list[schemas.PlaylistSong])
async def get_playlist_songs(
    playlist_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    playlist_songs = await playlist_facade.get_songs_in_playlist(playlist_id)
    return playlist_songs

@router.get('/songs/{song_id}/download')
async def download_song(song_id: int,
                        current_user: models.User = Depends(get_current_user)
                        ):
    song = await song_facade.get_song(song_id)
    file_data = await FILE_MANAGER.get_file(song.file_path)

    if not file_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')

    return Response(content=file_data,
                    media_type='application/octet-stream',
                    headers={'Content-Disposition': f"attachment; filename={os.path.basename(song.file_path)}"})