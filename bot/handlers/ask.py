from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.rag.service import RagService

router = Router()

@router.message(Command("ask"))
async def ask_handler(message: Message, rag: RagService) -> None:
    parts = (message.text or "").split(maxsplit=1)
    question = parts[1] if len(parts) == 2 else ""

    answer = await rag.answer(question)
    await message.answer(answer)