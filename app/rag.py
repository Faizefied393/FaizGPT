from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
VECTOR_DIR = BASE_DIR / "data" / "vectors"

for folder in [UPLOAD_DIR, VECTOR_DIR]:
    if folder.exists() and not folder.is_dir():
        raise RuntimeError(f"{folder} exists but is not a directory.")
    folder.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def simple_score(query: str, chunk: str) -> float:
    query_terms = query.lower().split()
    chunk_lower = chunk.lower()
    score = sum(chunk_lower.count(term) for term in query_terms)
    return float(score)


def index_text_file(file_path: Path) -> None:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    text = clean_text(text)
    chunks = chunk_text(text)

    payload = {
        "filename": file_path.name,
        "chunks": chunks
    }

    out_file = VECTOR_DIR / f"{file_path.stem}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def search_context(query: str, top_k: int = 3) -> str:
    results = []

    for file in VECTOR_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                payload = json.load(f)

            for chunk in payload.get("chunks", []):
                score = simple_score(query, chunk)
                if score > 0:
                    results.append((score, payload.get("filename", file.name), chunk))
        except Exception:
            continue

    results.sort(key=lambda x: x[0], reverse=True)
    top_results = results[:top_k]

    if not top_results:
        return ""

    combined = []
    for _, filename, chunk in top_results:
        combined.append(f"[Source: {filename}]\n{chunk}")

    return "\n\n".join(combined)