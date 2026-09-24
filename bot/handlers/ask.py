from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.rag.service import RagService

router = Router()

class AskState(StatesGroup):
    waiting_for_question = State()

@router.message(F.text == "Ask")
async def ask_button(message: Message, state: FSMContext) -> None:
    await state.set_state(AskState.waiting_for_question)
    await message.answer(
        "Please enter your question:\n"
        "To cancel, press Back.")

@router.message(AskState.waiting_for_question)
async def handler(
    message: Message,
    state: FSMContext,
    rag: RagService,
) -> None:
    parts = (message.text or "").split(maxsplit=1)
    question = parts[1].strip() if len(parts) == 2 else ""

    if not question:
        await state.set_state(AskState.waiting_for_question)
        await message.answer(
            "Please enter your question:\n"
            "To cancel, press Back."
        )
        return

    await message.answer("Searching for an answer...")
    answer = await rag.answer(question)
    await message.answer(answer)
    await state.clear()


@router.message (Command("ask"))
async def ask_from_button(
    message: Message,
    state: FSMContext,
    rag: RagService,
) -> None:
    question = (message.text or "").strip()

    if not question:
        await message.answer("Please enter a valid text question.")
        return

    await message.answer("Searching for an answer...")
    answer = await rag.answer(question)
    await message.answer(answer)
    await state.clear()