# Project 3: Lyrics Extraction Web App

A FastAPI app that extracts song lyrics by artist and title using the lyrics.ovh public API.

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to use the app.
