import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from the root .env file.")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
client = OpenAI(api_key=api_key)


def build_prompt(user_message: str, history: list[dict], context: str | None = None) -> str:
    system_text = (
        "You are FaizGPT, a clear, helpful, professional AI assistant. "
        "Be accurate, concise, beginner-friendly when needed, and structured."
    )

    prompt_parts = [f"SYSTEM:\n{system_text}\n"]

    if context:
        prompt_parts.append(f"DOCUMENT CONTEXT:\n{context}\n")

    if history:
        prompt_parts.append("CHAT HISTORY:")
        for msg in history[-10:]:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            prompt_parts.append(f"{role}: {content}")

    prompt_parts.append(f"USER:\n{user_message}")
    prompt_parts.append("ASSISTANT:")

    return "\n\n".join(prompt_parts)


def ask_faizgpt(user_message: str, history: list[dict], context: str | None = None) -> str:
    prompt = build_prompt(user_message, history, context)

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text