class RagService:
    def __init__(self, agent):
        self._agent = agent

    async def answer(self, question: str) -> str:
        question = question.strip()

        if not question:
            return (
                "Задайте вопрос после команды, например: "
                "/ask что такое рефакторинг"
            )

        result = await self._agent.arun(question)
        text = (result.content or "").strip()

        return text or (
            "Не нашёл ответа в учебнике. "
            "Попробуйте переформулировать вопрос."
        )