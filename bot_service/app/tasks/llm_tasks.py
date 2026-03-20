# bot_service/app/tasks/llm_tasks.py
print("DEBUG: llm_tasks.py был импортирован!")

import asyncio
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter
from aiogram import Bot
from app.core.config import settings

# Инициализируем бота для отправки ответа
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

# @celery_app.task(bind=True)
# def llm_request(self, chat_id: int, prompt: str):

#     print(f"Worker received task for chat {chat_id} with prompt: {prompt}")

#     # Запускаем асинхронную функцию в синхронном воркере
#     result = asyncio.run(call_openrouter(prompt))
    
#     # Отправляем результат пользователю
#     asyncio.run(bot.send_message(chat_id=chat_id, text=result))
#     return result

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