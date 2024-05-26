from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    email: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password:str


class User(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class ArtistBase(BaseModel):
    name: str
    description: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: int

    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    title: str
    description: str
    artist_id: int


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int

    class Config:
        from_attributes = True


class SongBase(BaseModel):
    title: str
    text: str
    album_id: int

    class Config:
        from_attributes = True


class SongCreate(SongBase):
    genres: List[int]

    class Config:
        from_attributes = True


class Song(SongBase):
    id: int

    class Config:
        from_attributes = True


class FavouriteSongBase(BaseModel):
    song_id: int
    user_id: int


class FavouriteSongCreate(BaseModel):
    song_id: int


class FavouriteSong(FavouriteSongBase):

    class Config:
        from_attributes = True


class PlaylistBase(BaseModel):
    name: str
    user_id: int

    class Config:
        from_attributes = True


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    id: int

    class Config:
        from_attributes = True


class PlaylistSongBase(BaseModel):
    song_id: int
    playlist_id: int


class PlaylistSongCreate(BaseModel):
    song_id: int
    playlist_id: int


class PlaylistSong(PlaylistSongBase):

    class Config:
        from_attributes = True