import os

from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from dotenv import load_dotenv

load_dotenv()


KB_DATABASE_URL = os.getenv("KB_DATABASE_URL")
if not KB_DATABASE_URL:
    raise RuntimeError(
        "KB_DATABASE_URL is not set. Add it to .env or environment variables."
    )

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. "
        "Add it to .env or environment variables."
    )

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "openai/text-embedding-3-small",
)
EMBEDDING_DIMENSIONS = int(
    os.getenv("EMBEDDING_DIMENSIONS", "1536")
)

embedder = OpenAIEmbedder(
    id=EMBEDDING_MODEL,
    dimensions=EMBEDDING_DIMENSIONS,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    enable_batch=True,
    batch_size=100,
)

vector_db = PgVector(
    table_name="knowledge",
    db_url=KB_DATABASE_URL,
    embedder=embedder,
)

knowledge = Knowledge(
    vector_db=vector_db,
)