import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_store")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing in .env file")