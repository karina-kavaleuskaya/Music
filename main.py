from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from facade.artist_facade import artist_facade
from facade.genre_facade import genre_facade
from facade.album_facade import album_facade
from facade.song_facade import song_facade
from facade.favourite_song_facade import favourite_song_facade
from facade.playlist_facade import playlist_facade
from async_db import get_db
import users
import admin
import views


def set_db_for_facades(db):
    artist_facade.set_db(db)
    genre_facade.set_db(db)
    album_facade.set_db(db)
    song_facade.set_db(db)
    favourite_song_facade.set_db(db)
    playlist_facade.set_db(db)


OAuth2_SCHEME = OAuth2PasswordBearer('user/login/')

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    async for db in get_db():
        set_db_for_facades(db)
        break


app.include_router(users.router)
app.include_router(admin.router)
app.include_router(views.router)


@app.get('/')
async def index():
    return {'message': 'Hello World'}