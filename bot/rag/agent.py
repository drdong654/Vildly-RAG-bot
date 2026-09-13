from agno.agent import Agent
from agno.models.ollama import Ollama

from bot.rag.knowledge import knowledge


def build_agent() -> Agent:
    return Agent(
        model=Ollama(id="qwen3:4b"),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=(
            "Отвечай только на основе учебника. "
            "Если в учебнике нет ответа, так и скажи."
        ),
        markdown=True,
    )