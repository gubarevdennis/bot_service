# bot_service/app/bot/handlers.py
from aiogram import Router, types
from aiogram.filters import Command
from app.core.jwt import decode_and_validate
from app.infra.redis import redis_client
from app.tasks.llm_tasks import llm_request

router = Router()

@router.message(Command("token"))
async def handle_token(message: types.Message):
    # Команда /token <jwt>
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Пожалуйста, отправьте токен: /token <ваш_jwt>")
        return
    
    token = args[1]
    try:
        # Проверяем токен перед сохранением
        decode_and_validate(token)
        # Сохраняем в Redis: ключ token:<tg_user_id>
        await redis_client.set(f"token:{message.from_user.id}", token)
        await message.answer("Токен принят и сохранен!")
    except Exception as e:
        await message.answer(f"Ошибка валидации токена: {e}")

@router.message(Command("logout"))
async def cmd_logout(message: types.Message):
    user_id = message.from_user.id
    # Удаляем токен из Redis
    await redis_client.delete(f"token:{user_id}")
    await message.answer("Вы вышли из системы. Чтобы авторизоваться снова, используйте /token <jwt>")


@router.message()
async def handle_message(message: types.Message):
    # 1. Получаем токен из Redis
    token = await redis_client.get(f"token:{message.from_user.id}")
    if not token:
        await message.answer("Токен не найден. Пожалуйста, авторизуйтесь через /token <jwt>")
        return
    
    # 2. Валидируем токен (пока он в Redis, он может уже истечь!)
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Ваш токен истек или невалиден. Пожалуйста, получите новый.")
        return
    
    # 3. Отправляем задачу в Celery (RabbitMQ)
    llm_request.delay(chat_id=message.chat.id, prompt=message.text)
    await message.answer("Запрос принят в работу, ожидайте ответа...")

