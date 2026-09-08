from agno.agent import Agent
from agno.models.ollama import Ollama

from AI.config import OLLAMA_HOST


def build_agent() -> Agent:
    return Agent(
        model=Ollama(
            id="qwen3:4b",
            host=OLLAMA_HOST,
        ),
        instructions=[
            "Отвечай только по переданному контексту.",
            "Не добавляй информацию из общей памяти.",
            "Если контекст не содержит ответа, сообщи об этом.",
            "В конце укажи источник и страницу.",
        ],
        markdown=True,
    )