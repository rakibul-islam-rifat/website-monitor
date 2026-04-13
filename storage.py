import json
import logging
from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)
root_folder: Path = Path(__file__).parent
HASH_FILE: Path = root_folder / "hashes.json"


def load_hashes() -> dict:
    if HASH_FILE.is_file():
        with open(HASH_FILE, encoding="utf-8") as rf:
            return json.load(rf)

    return {}


def save_hashes(data: dict) -> None:
    with open(HASH_FILE, "w", encoding="utf-8") as wf:
        json.dump(data, wf, indent=2)


def has_changed(stored_hash: str, current_hash: str) -> bool:
    return stored_hash != current_hash
