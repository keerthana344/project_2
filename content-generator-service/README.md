# Project 2: AI-Powered Content Generator & Analyzer

A FastAPI app that generates social media content and analyzes its sentiment using OpenAI GPT-4.

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
3. Add your OpenAI API key to the `.env` file.

## Run

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test.
