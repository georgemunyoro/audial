import sqlite3

default_con = sqlite3.connect("audial.db")


def ensure_db_tables_exist(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        for i in ("sources", "tracks", "playlists", "playlist_track"):
            c.execute(
                f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{i}'"
            )
            if c.fetchone()[0] != 1:
                print(f"{i} table not found in database...creating table.")
                if i == "sources":
                    create_sources_table()
                if i == "tracks":
                    create_tracks_table()
                if i == "playlists":
                    create_playlists_table()
                if i == "playlist_track":
                    create_playlist_track_table()
                print(f"{i} table created successfully!")


def create_sources_table(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute("CREATE TABLE sources (path text)")


def create_tracks_table(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute(
            """CREATE TABLE tracks (id text, title text, artist text, album text, album_artist text, track_num int, file text)"""
        )


def create_playlists_table(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute("""CREATE TABLE playlists (id text, title text)""")


def create_playlist_track_table(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute(
            """CREATE TABLE playlist_track (id text, playlist text, track text)"""
        )


def insert_playlists(playlists, db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()

        for i in playlists:
            p_id = i["id"]
            p_title = i["title"]
            c.execute(f"""INSERT INTO playlists VALUES ('{p_id}', '{p_title}')""")


def insert_tracks(tracks, db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()

        for i in tracks:
            if i[5] is None:
                i[5] = 1
            row = "(" + ",".join([repr(j) for j in i if j != None]) + ")"
            c.execute(f"""INSERT INTO tracks VALUES {row}""")


def get_playlists(db="audial.db"):
    playlists = []
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute("SELECT * FROM PLAYLISTS WHERE 1 == 1")
        x = c.fetchall()

        for i in x:
            playlists.append(({"id": i[0], "title": i[1]}))

    return playlists


def get_tracks(db="audial.db"):
    tracks = []
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute("SELECT * FROM TRACKS WHERE 1 == 1")

        x = c.fetchall()

        for i in x:
            t_id, title, artist, album, album_artist, track_num, fpath = i
            tracks.append(
                {
                    "id": t_id,
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "album_artist": album_artist,
                    "track_num": track_num,
                    "file": fpath,
                }
            )

    return tracks


def get_track(t_id, db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute(f"SELECT * FROM tracks WHERE id = '{t_id}'")

        return c.fetchone()


def get_sources(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute("SELECT * FROM sources WHERE 1 == 1")
        return [i[0] for i in c.fetchall()]
