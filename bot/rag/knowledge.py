import os

from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from dotenv import load_dotenv

load_dotenv()

KB_DATABASE_URL = os.getenv("KB_DATABASE_URL")
if not KB_DATABASE_URL:
    raise RuntimeError(
        "KB_DATABASE_URL is not set. Add it to .env or environment variables."
    )
embedder = OllamaEmbedder(
    id="nomic-embed-text", 
    dimensions=768
    )
vector_db = PgVector(
    table_name="knowledge",
    db_url=KB_DATABASE_URL,
    embedder=embedder,
)

knowledge = Knowledge(
    vector_db=vector_db,
)