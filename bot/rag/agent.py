import os

from agno.agent import Agent
from agno.models.openrouter import OpenRouter

from bot.rag.knowledge import knowledge


def build_model() -> OpenRouter:
    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    model_id = os.getenv("LLM_MODEL", "openrouter/free")

    return OpenRouter(id=model_id)

def build_agent() -> Agent:
    return Agent(
        model=build_model(),

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
