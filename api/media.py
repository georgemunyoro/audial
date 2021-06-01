# -*- coding: utf-8 -*-
import db
import os
import uuid
from pathlib import Path
from eyed3.mp3 import Mp3AudioFile
import utils


def create_playlist(playlist_name: str) -> None:
    db.insert_playlists([{"id": str(uuid.uuid4()), "title": playlist_name}])


def add_source(sources=[]):
    for source in sources:
        if source in db.get_sources():
            print(f"Source already exists!: '{source}'")
            return

    with db.default_con:
        c = db.default_con.cursor()
        c.execute(
            f"""INSERT INTO sources VALUES {" ".join([f"('{i}')" for i in sources])}"""
        )


def remove_source(source):
    if source not in db.get_sources():
        print("No such media source exists!")
        return

    if (
        input(f"Are you sure you want to remove source '{source}'? [y/N]").lower()
        == "y"
    ):
        with db.default_con:
            c = db.default_con.cursor()
            c.execute(f"DELETE FROM sources WHERE path='{source}'")

            print("Source has been removed successfully")


def list_sources():
    print(f"{len(db.get_sources())} source(s) found: ")

    for source in db.get_sources():
        print(source)


def list_playlists():
    print(f"{len(db.get_playlists())} playlist(s) found: ")

    for playlist in db.get_playlists():
        print(playlist)


def scan_sources():
    print("Scanning media sources...")

    tracks = []
    for source in db.get_sources():
        for i in os.listdir(source):
            if i.split(".").pop() == "mp3":
                if source[-1] != "/":
                    source += "/"
                mp3 = Mp3AudioFile(source + i)

                try:
                    title = mp3.tag.title
                    artist = mp3.tag.artist
                    album = mp3.tag.album
                    album_artist = mp3.tag.album_artist
                    track_num = mp3.tag.track_num
                    image = mp3.tag.images[0]

                    track_id = str(uuid.uuid4())
                    cache_dir = utils.cache_dir()

                    if "audial" not in os.listdir(cache_dir):
                        os.mkdir(f"{cache_dir}/audial")
                        os.mkdir(f"{cache_dir}/audial/imgs")

                    with open(f"{cache_dir}/audial/imgs/{track_id}.jpg", "wb") as f:
                        f.write(image.image_data)

                    if title is None:
                        title = ""
                    if artist is None:
                        artist = ""
                    if album is None:
                        album = ""
                    if album_artist is None:
                        album_artist = ""
                    if track_num is None:
                        track_num = 1

                    if len(track_num) == 2:
                        track_num = track_num[0]

                    tracks.append(
                        [
                            track_id,
                            title,
                            artist,
                            album,
                            album_artist,
                            track_num,
                            source + i,
                        ]
                    )

                except UnicodeEncodeError:
                    pass
                except AttributeError:
                    # object is none
                    print(i)
                    pass
                except IndexError:
                    # no images
                    try:
                        print(i)
                    except UnicodeEncodeError:
                        pass
                    pass

        db.insert_tracks(tracks)
