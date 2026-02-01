import json
from functools import lru_cache
from pathlib import Path


@lru_cache
def _load_preset_words() -> dict[str, list[str]]:
    path = Path(__file__).resolve().parent / "data" / "preset_words.json"
    with path.open() as handle:
        return json.load(handle)


def get_preset_words(goal: str) -> list[str]:
    data = _load_preset_words()
    words = data.get(goal)
    if words is None:
        raise ValueError(f"unknown goal: {goal}")
    return words
