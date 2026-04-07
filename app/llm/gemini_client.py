import json
import re

import google.generativeai as genai

from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


async def ask_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


async def ask_gemini_json(prompt: str):
    raw = await ask_gemini(prompt)

    # essaie d'extraire un JSON objet ou liste
    match = re.search(r"(\{.*\}|\[.*\])", raw, re.S)
    if not match:
        raise ValueError(f"Réponse Gemini non JSON: {raw}")

    return json.loads(match.group(1))
