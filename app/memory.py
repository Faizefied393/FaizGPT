import json
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent
CHAT_DIR = BASE_DIR / "data" / "chats"

if CHAT_DIR.exists() and not CHAT_DIR.is_dir():
    raise RuntimeError(f"{CHAT_DIR} exists but is not a directory.")

CHAT_DIR.mkdir(parents=True, exist_ok=True)


def _chat_file(session_id: str) -> Path:
    return CHAT_DIR / f"{session_id}.json"


def load_history(session_id: str) -> List[dict]:
    file_path = _chat_file(session_id)
    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(session_id: str, history: List[dict]) -> None:
    file_path = _chat_file(session_id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def append_message(session_id: str, role: str, content: str) -> List[dict]:
    history = load_history(session_id)
    history.append({"role": role, "content": content})
    save_history(session_id, history)
    return history
