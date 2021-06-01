import subprocess
import argparse

from dotenv.main import load_dotenv
import media
import os
from shutil import rmtree
import db
import utils
import pprint


load_dotenv()
API_PORT = str(os.getenv("API_PORT"))


def start_http_server(_dir=utils.temp_dir()):
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=_dir)


def handle_args(args):
    global API_PORT

    if args.__contains__("add_source") and args.add_source:
        media.add_source(args.add_source)
    if args.__contains__("list_sources") and args.list_sources:
        media.list_sources()
    if args.__contains__("remove_source") and args.remove_source:
        media.remove_source(args.remove_source)
    if args.__contains__("scan_sources") and args.scan_sources:
        media.scan_sources()
    if args.__contains__("list_tracks") and args.list_tracks:
        query = args.list_tracks

        print("-" * os.get_terminal_size()[0])

        def print_track(track: dict) -> None:
            for i in track.keys():
                ftd_string = "{0:>15}".format(i)
                print(f"{ftd_string}: {track[i]}")
            print("-" * os.get_terminal_size()[0])

        matches = 0

        for track in db.get_tracks():
            match = False
            for i in ["title", "artist", "album", "album_artist"]:
                if query.lower() in track[i].lower():
                    match = True
            if match:
                print_track(track)
                matches += 1

        print(f"Matches Found: {matches}")

    if args.__contains__("run") and args.run:

        temp_dir = utils.temp_dir()

        try:
            rmtree(temp_dir)
        except:
            pass

        os.mkdir(temp_dir)
        subprocess.Popen(
            ["uvicorn server:server --host 0.0.0.0 & > /dev/null"],
            shell=True,
            stdin=None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )

        subprocess.Popen(
            [f"cd /tmp/audial && python3 -m http.server {API_PORT}"],
            shell=True,
            stdin=None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )

    if args.__contains__("stop"):
        os.system("fuser -n tcp -k 8000")
        os.system(f"fuser -n tcp -k {API_PORT}")


def main():
    db.ensure_db_tables_exist()

    parser = argparse.ArgumentParser(prog="audial", description="Music Server")
    subparsers = parser.add_subparsers()

    parser.version = os.getenv("APP_VERSION")

    server_p = subparsers.add_parser("server")
    server_p.add_argument("-p", "--port")
    server_p.add_argument("-a", "--address")
    server_p.add_argument("-r", "--run", action="store_true")
    server_p.add_argument("-s", "--stop", action="store_true")

    media_p = subparsers.add_parser("media")
    media_p.add_argument("-l", "--list-sources", action="store_true")
    media_p.add_argument("-a", "--add-source", metavar="<MEDIA_SOURCES>", nargs="+")
    media_p.add_argument("-s", "--scan-sources", action="store_true")
    media_p.add_argument("-r", "--remove-source", metavar="<SOURCE_PATH>")

    media_p.add_argument("-lt", "--list-tracks", action="store")

    parser.add_argument("-c", "--config-file", action="store")
    parser.add_argument("-v", "--version", action="version")

    handle_args(parser.parse_args())


if __name__ == "__main__":
    main()
