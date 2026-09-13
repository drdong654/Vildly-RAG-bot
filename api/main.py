# api/main.py
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv

from bot.db.engine import make_sessionmaker, init_models
from bot.db.repositories.users import UserRepository

from sqladmin import Admin
from api.admin import UserAdmin

from pydantic import BaseModel, Field

from AI.agent import build_agent
from AI.knowledge import knowledge
from AI.service import RagService

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add DATABASE_URL to environment variables.")

engine, Session = make_sessionmaker(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine)
    yield


app = FastAPI(title="vildly-rag-bot API", lifespan=lifespan)


admin = Admin(app, engine)
admin.add_view(UserAdmin)

async def get_users():
    async with Session() as session:
        yield UserRepository(session)             # тот же репозиторий, что у бота

@app.get("/users")
async def list_users(users: UserRepository = Depends(get_users)):
    return await users.list_all()

@app.get("/users/{telegram_id}")
async def get_user(telegram_id: int, users: UserRepository = Depends(get_users)):
    user = await users.get_by_telegram_id(telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

rag_service = RagService(
    knowledge=knowledge,
    agent=build_agent(),
)
class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class AskResponse(BaseModel):
    answer: str


class SearchRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class SearchHit(BaseModel):
    content: str
    source: str | None
    page: int | None
    score: float | None

@app.post("/search", response_model=list[SearchHit])
async def search_knowledge(body: SearchRequest):
    try:
        results = await rag_service.search(
            question=body.question,
            limit=body.limit,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return [SearchHit(**result) for result in results]


@app.post("/ask", response_model=AskResponse)
async def ask_question(body: AskRequest):
    try:
        answer = await rag_service.answer(body.question)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return AskResponse(answer=answer)
