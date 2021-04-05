# -*- coding: utf-8 -*-
from typing import Optional
from shutil import copyfile, rmtree
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sqlite3
import os
import db
import spotipy
from dotenv import load_dotenv

load_dotenv()

server = FastAPI()
s_con = sqlite3.connect("audial.db")

spotify_credentials = spotipy.SpotifyClientCredentials(
    client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET")
)
spotify = spotipy.Spotify(client_credentials_manager=spotify_credentials)

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

    rmtree("/tmp/audial")
    os.mkdir("/tmp/audial")

    ext = fpath.split(".").pop()

    copyfile(fpath, f"/tmp/audial/{t_id}.{ext}")
    copyfile(f"{Path.home()}/.cache/audial/imgs/{t_id}.jpg", f"/tmp/audial/{t_id}.jpg")
    return {
        "track": f"http://localhost:4242/{t_id}.{ext}",
        "art": f"http://localhost:4242/{t_id}.jpg",
    }


# @server.post("/music/{track_id}")
# def play_track(track_id):
#     db.get


@server.get("/sources")
def sources():
    return db.get_sources()


def main():
    print(spotify.playlist("4ehqP8QHaIPdHMsssoB4y2"))


if __name__ == "__main__":
    main()
