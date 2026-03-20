# auth_service/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Auth Service", lifespan=lifespan)

# Подключаем роуты
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}