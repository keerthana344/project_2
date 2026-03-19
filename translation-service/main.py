from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Real-Time Translation Service", description="Translates text using OpenAI GPT-4.")
templates = Jinja2Templates(directory="templates")

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    target_language: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key is missing. Set OPENAI_API_KEY in .env.")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that strictly translates text to {request.target_language}."},
                {"role": "user", "content": request.text}
            ],
            temperature=0.3
        )
        translated_text = response.choices[0].message.content.strip()
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            target_language=request.target_language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
