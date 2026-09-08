import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

PDF_PATH = Path(
    os.getenv("PDF_PATH", BASE_DIR / "assets" / "Sommerville.pdf")
).resolve()

KB_DATABASE_URL = os.getenv(
    "KB_DATABASE_URL",
    "postgresql+psycopg://bot:123@localhost:5432/bot",
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)

KNOWLEDGE_TABLE = "knowledge"

CHUNK_SIZE = 4000
CHUNK_OVERLAP = 400