import sqlite3

default_con = sqlite3.connect("audial.db")


def ensure_db_tables_exist(db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sources'"
        )
        if c.fetchone()[0] != 1:
            print("Sources table not found in database...creating table.")
            create_sources_table()
            print("Sources table created successfully!")

        c.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tracks'"
        )
        if c.fetchone()[0] != 1:
            print("Tracks table not found in database...creating table.")
            create_tracks_table()
            print("Tracks table created successfully!")


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


def insert_tracks(tracks, db="audial.db"):
    with sqlite3.connect(db) as con:
        c = con.cursor()

        for i in tracks:
            if i[5] is None: i[5] = 1
            row = "(" + ",".join([repr(j) for j in i if j != None]) + ")"
            c.execute(f"""INSERT INTO tracks VALUES {row}""")


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
