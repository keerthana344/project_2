# Project 4: Image to Text OCR API

A FastAPI app that extracts text from uploaded images using PyTesseract OCR.

## Prerequisites

- **Tesseract-OCR** must be installed on your system.
  - Download from: https://github.com/UB-Mannheim/tesseract/wiki
  - After installing, add the Tesseract install path to your system PATH.

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

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to upload an image.
