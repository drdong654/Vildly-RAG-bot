import os

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.openrouter import OpenRouter

from bot.rag.knowledge import knowledge


def build_model():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    model_id = os.getenv("LLM_MODEL")

    if provider == "openrouter":
        if not os.getenv("OPENROUTER_API_KEY"):
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        return OpenRouter(
            id=model_id or "openrouter/free",
        )
    if provider == "ollama":
        return Ollama(
            id=model_id or "qwen3:4b",
            host=os.getenv("OLLAMA_HOST"),
        )
    raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider}")

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
