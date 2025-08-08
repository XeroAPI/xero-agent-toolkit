import os

import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DB_URL = f"sqlite:///./sessions.db"
ALLOWED_ORIGINS = ["http://localhost","http://localhost:8080","*"]
SERVE_WEB_INTERFACE = True

app: FastAPI = get_fast_api_app(
    agents_dir=APP_DIR,
    session_db_url=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))