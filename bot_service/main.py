# bot_service/app/main.py
from fastapi import FastAPI
from app.bot.dispatcher import dp, bot
from app.bot.handlers import router as bot_router

app = FastAPI(title="Bot Service")

# Регистрируем хэндлеры
dp.include_router(bot_router)

@app.on_event("startup")
async def startup():
    # Запускаем поллинг (в реальном проекте используйте вебхуки)
    # Для простоты разработки поллинг запускаем в фоне
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

@app.get("/health")
async def health():
    return {"status": "ok"}