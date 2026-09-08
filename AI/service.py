from typing import Any

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge


class RagService:
    def __init__(self, knowledge: Knowledge, agent: Agent):
        self._knowledge = knowledge
        self._agent = agent

    async def search(
        self,
        question: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        question = question.strip()

        if not question:
            raise ValueError("Вопрос не должен быть пустым")

        documents = await self._knowledge.asearch(
            query=question,
            max_results=limit,
        )

        results = []

        for document in documents:
            metadata = document.meta_data or {}

            results.append(
                {
                    "content": document.content,
                    "source": document.name,
                    "page": metadata.get("page"),
                    "score": metadata.get("similarity_score"),
                }
            )

        return results

    async def answer(self, question: str) -> str:
        question = question.strip()

        if not question:
            raise ValueError("Вопрос не должен быть пустым")

        hits = await self.search(question, limit=3)

        if not hits:
            return "В базе знаний не найден релевантный контекст."

        context_parts = []

        for hit in hits:
            context_parts.append(
                f"[Источник: {hit['source']}, страница: {hit['page']}]\n"
                f"{hit['content']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
Ответь на вопрос, используя только приведённый контекст.

Контекст:
{context}

Вопрос:
{question}
""".strip()

        response = await self._agent.arun(prompt)
        answer = str(response.content or "").strip()

        return answer or "Не удалось сформировать ответ."