# bot_service/app/tasks/llm_tasks.py
import asyncio
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter
from aiogram import Bot
from app.core.config import settings

# Инициализируем бота для отправки ответа
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

@celery_app.task(bind=True)
def llm_request(self, chat_id: int, prompt: str):
    # Запускаем асинхронную функцию в синхронном воркере
    result = asyncio.run(call_openrouter(prompt))
    
    # Отправляем результат пользователю
    asyncio.run(bot.send_message(chat_id=chat_id, text=result))
    return result