# bot_service/app/tasks/llm_tasks.py
import asyncio
import logging
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter
from aiogram import Bot
from app.core.config import settings

# Инициализируем бота для отправки ответа
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

# Настройка логирования вместо print
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("llm_tasks.py был импортирован!")

# Функция, которая содержит всю асинхронную логику
async def async_llm_logic(chat_id, prompt):
    # 1. Запрос к LLM
    response_text = await call_openrouter(prompt)
    
    # 2. Отправка в Telegram
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=response_text)
    await bot.session.close() # Обязательно закрываем сессию!

@celery_app.task
def llm_request(chat_id, prompt):
    # Запускаем асинхронную логику в новом цикле событий
    asyncio.run(async_llm_logic(chat_id, prompt))