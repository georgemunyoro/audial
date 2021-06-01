# -*- coding: utf-8 -*-
from typing import Optional
from shutil import copyfile, rmtree
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sqlite3
import os

from spotipy import util
import db
import spotipy
from dotenv import load_dotenv
import socket
import utils

load_dotenv()

server = FastAPI()
s_con = sqlite3.connect("audial.db")

spotify_credentials = spotipy.SpotifyClientCredentials(
    client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET")
)
spotify = spotipy.Spotify(client_credentials_manager=spotify_credentials)

API_PORT = str(os.getenv("API_PORT"))

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@server.get("/")
def root():
    return {"message": "ok"}


@server.get("/music")
def music(skip: int = 0, limit: int = 100, artist: str = None):
    if artist:
        return [i for i in db.get_tracks() if i["artist"] == artist][
            skip : skip + limit
        ]
    return db.get_tracks()[skip : skip + limit]


@server.get("/music/{track_id}")
def track(track_id):
    i = db.get_track(t_id=track_id)
    print(i)
    t_id, title, artist, album, album_artist, track_num, fpath = i

    cache_dir = utils.cache_dir()
    temp_dir = utils.temp_dir()

    rmtree(temp_dir)
    os.mkdir(temp_dir)

    ext = fpath.split(".").pop()

    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)

    copyfile(fpath, f"{temp_dir}/{t_id}.{ext}")
    copyfile(f"{cache_dir}/audial/imgs/{t_id}.jpg", f"{cache_dir}/{t_id}.jpg")

    return {
        "track": f"http://{utils.ip_addr()}:{API_PORT}/{t_id}.{ext}",
        "art": f"http://{utils.ip_addr()}:{API_PORT}/{t_id}.jpg",
    }


@server.get("/sources")
def sources():
    return db.get_sources()


if __name__ == "__main__":
    main()
