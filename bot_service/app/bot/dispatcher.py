# bot_service/app/bot/dispatcher.py
from aiogram import Bot, Dispatcher
from app.core.config import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()