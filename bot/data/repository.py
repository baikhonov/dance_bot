import json
from pathlib import Path


_CONTENT_PATH = Path(__file__).resolve().parent / "content.json"
_CACHE = None


def get_content():
    global _CACHE
    if _CACHE is None:
        with _CONTENT_PATH.open("r", encoding="utf-8") as file:
            _CACHE = json.load(file)
    return _CACHE
