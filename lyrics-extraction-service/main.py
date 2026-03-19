from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx

app = FastAPI(title="Lyrics Extraction Web App", description="Extracts lyrics for a given artist and song title.")
templates = Jinja2Templates(directory="templates")

class LyricsResponse(BaseModel):
    artist: str
    song_title: str
    lyrics: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/lyrics", response_model=LyricsResponse)
async def get_lyrics(artist: str, song_title: str):
    url = f"https://api.lyrics.ovh/v1/{artist}/{song_title}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=15.0)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Lyrics not found for this song.")
        response.raise_for_status()
        data = response.json()
        return LyricsResponse(
            artist=artist,
            song_title=song_title,
            lyrics=data.get("lyrics", "")
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
