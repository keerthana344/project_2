from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Content Generator & Analyzer", description="Generates content and analyzes sentiment.")
templates = Jinja2Templates(directory="templates")

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class ContentRequest(BaseModel):
    topic: str

class ContentResponse(BaseModel):
    topic: str
    generated_content: str
    sentiment: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_model=ContentResponse)
async def generate_and_analyze(request: ContentRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key is missing. Set OPENAI_API_KEY in .env.")
    try:
        content_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative social media manager. Generate a short, engaging tweet about the provided topic."},
                {"role": "user", "content": request.topic}
            ],
            temperature=0.7
        )
        generated_content = content_response.choices[0].message.content.strip()

        sentiment_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sentiment analyzer. Reply with exactly one word: POSITIVE, NEGATIVE, or NEUTRAL."},
                {"role": "user", "content": generated_content}
            ],
            temperature=0.0
        )
        sentiment = sentiment_response.choices[0].message.content.strip()

        return ContentResponse(
            topic=request.topic,
            generated_content=generated_content,
            sentiment=sentiment
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
