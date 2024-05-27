import models
import schemas
from users import get_current_user
from fastapi import HTTPException, status, Depends, APIRouter, Form, UploadFile, File
from facade.artist_facade import artist_facade
from facade.genre_facade import genre_facade
from facade.album_facade import album_facade
from facade.song_facade import song_facade
from facade.facade import FILE_MANAGER
from pathlib import Path

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


UPLOAD_DIRECTORY = 'static/songs/'
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)


HTTP_EXCEPTION_FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have admin permission"
)


@router.post('/artists/', response_model=schemas.Artist)
async def create_artist(
        artist_data: schemas.ArtistCreate,
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTP_EXCEPTION_FORBIDDEN

    db_artist = await artist_facade.create_artist(artist_data)

    return db_artist


@router.post('/genres/', response_model=schemas.Genre)
async def create_genre(
        genre_data: schemas.GenreCreate,
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTP_EXCEPTION_FORBIDDEN

    db_genre = await genre_facade.create_genre(genre_data)

    return db_genre

@router.post('/albums/', response_model=schemas.Album)
async def create_album(
        album_data: schemas.AlbumCreate,
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTP_EXCEPTION_FORBIDDEN

    db_album = await album_facade.create_album(album_data)

    return db_album


@router.post('/songs/', response_model=schemas.Song)
async def create_song(
        title: str = Form(...),
        text: str = Form(...),
        album_id: int = Form(...),
        genres: str = Form(...),
        file: UploadFile = File(...),
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTP_EXCEPTION_FORBIDDEN

    file_path = f'static/songs/{file.filename}'
    await FILE_MANAGER.save_file(file, file_path)

    genres_list = [int(genre_id) for genre_id in genres.split(",")]

    song_data = schemas.SongCreate(
        title=title,
        text=text,
        album_id=album_id,
        genres=genres_list
    )
    db_song = await song_facade.create_song(song_data, file_path)

    return db_song


@router.delete('/songs/{song_id}/')
async def delete_song(
        song_id: int,
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTP_EXCEPTION_FORBIDDEN

    await song_facade.delete_song(song_id)