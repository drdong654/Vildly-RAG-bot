import asyncio

from bot.rag.knowledge import knowledge

async def main() -> None:
    await knowledge.ainsert(
        path="knowledge/sommerville",
        include=["*.pdf"],
        skip_if_exists=True,
    )
    print("Учебник проиндексирован")

if __name__ == "__main__":
    asyncio.run(main())