import pytest
from unittest.mock import AsyncMock, MagicMock
from app.bot.handlers import handle_token, handle_message
from app.infra.redis import redis_client

@pytest.mark.asyncio
async def test_handle_token_saves_to_redis(mocker):
    # Мокаем валидацию
    mocker.patch("app.bot.handlers.decode_and_validate", return_value={"sub": "123"})
    mocker.patch.object(redis_client, 'set', new_callable=AsyncMock)
    
    # Создаем Mock-сообщение вместо реального Pydantic-объекта
    message = MagicMock()
    message.from_user.id = 123
    message.text = "/token my_jwt"
    message.answer = AsyncMock()
    
    await handle_token(message)
    
    redis_client.set.assert_called_once_with("token:123", "my_jwt")
    message.answer.assert_called_with("Токен принят и сохранен!")

@pytest.mark.asyncio
async def test_handle_message_triggers_celery(mocker):
    # Мокаем Redis
    mocker.patch.object(redis_client, 'get', new_callable=AsyncMock, return_value="my_jwt")
    # Мокаем валидацию
    mocker.patch("app.bot.handlers.decode_and_validate", return_value={"sub": "123"})
    # Мокаем Celery
    mock_delay = mocker.patch("app.tasks.llm_tasks.llm_request.delay")
    
    # Создаем Mock-сообщение
    message = MagicMock()
    message.from_user.id = 123
    message.chat.id = 123
    message.text = "Hello"
    message.answer = AsyncMock()
    
    await handle_message(message)
    
    mock_delay.assert_called_once_with(chat_id=123, prompt="Hello")
    message.answer.assert_called_with("Запрос принят в работу, ожидайте ответа...")