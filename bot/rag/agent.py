import os

from agno.agent import Agent
from agno.models.ollama import Ollama

from bot.rag.knowledge import knowledge


def build_agent() -> Agent:
    return Agent(
        model=Ollama(
            id="qwen3:4b",
            host=os.getenv("OLLAMA_HOST"),
        ),
        knowledge=knowledge,
        search_knowledge=True,

        instructions=(
            "Отвечай только на основе найденных фрагментов учебника. "
            "Не добавляй внешние факты, примеры или числовые оценки. "
            "Сначала дай краткий прямой ответ на вопрос. "
            "Указывай страницы источника, если они известны. "
            "Отвечай на языке, на котором задан вопрос. "
            "Если найденных фрагментов недостаточно, честно скажи об этом."
        ),
        markdown=True,
    )
