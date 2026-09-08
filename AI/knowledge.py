from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType

from AI.config import (
    EMBEDDING_MODEL,
    KB_DATABASE_URL,
    KNOWLEDGE_TABLE,
    OLLAMA_HOST,
)

embedder = OllamaEmbedder(
    id=EMBEDDING_MODEL,
    dimensions=768,
    host=OLLAMA_HOST,
)
vector_db = PgVector(
    table_name=KNOWLEDGE_TABLE,
    db_url=KB_DATABASE_URL,
    embedder=embedder,
    search_type=SearchType.hybrid,
)
knowledge = Knowledge(
    vector_db=vector_db,
    max_results=3,
)