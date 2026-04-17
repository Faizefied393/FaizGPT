from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse, UploadResponse
from app.memory import load_history, append_message
from app.llm import ask_faizgpt
from app.rag import index_text_file, search_context

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

if UPLOAD_DIR.exists() and not UPLOAD_DIR.is_dir():
    raise RuntimeError(f"{UPLOAD_DIR} exists but is not a directory.")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="FaizGPT API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "FaizGPT backend is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history = load_history(request.session_id)
    context = search_context(request.message)

    try:
        response_text = ask_faizgpt(
            user_message=request.message,
            history=history,
            context=context if context else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    append_message(request.session_id, "user", request.message)
    append_message(request.session_id, "assistant", response_text)

    return ChatResponse(response=response_text)


@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    allowed_suffixes = {".txt", ".md"}
    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed_suffixes:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are supported in this version."
        )

    save_path = UPLOAD_DIR / file.filename
    content = await file.read()

    with open(save_path, "wb") as f:
        f.write(content)

    index_text_file(save_path)

    return UploadResponse(
        filename=file.filename,
        message="File uploaded and indexed successfully."
    )