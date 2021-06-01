import os
import socket
import sys
from pathlib import Path

from dotenv.main import load_dotenv

load_dotenv()

def cache_dir() -> str:
    if sys.platform == "win32":
        return f"{Path.home()}/AppData/Roaming"
    elif sys.platform == "linux":
        return f"{Path.home()}/.cache"


def temp_dir() -> str:
    if sys.platform == "win32":
        return f"{Path.home()}/AppData/Local/Temp/audial"
    elif sys.platform == "linux":
        return f"/tmp/audial"


def ip_addr() -> str:
    if os.getenv("SERVER_IP") != None:
        return os.getenv("SERVER_IP")

    ip = (
        (
            [
                ip
                for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")
            ]
            or [
                [
                    (s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                ][0][1]
            ]
        )
        + ["no IP found"]
    )[0]
