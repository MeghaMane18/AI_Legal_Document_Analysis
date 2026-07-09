import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    UPLOAD_FOLDER = "uploads"
    CHROMA_DB_PATH = "chroma_db"

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB