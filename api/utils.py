from pathlib import Path
import sys


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
