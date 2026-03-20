import pytest
from app.core.jwt import decode_and_validate
from app.core.config import settings

# Тест будет использовать фикстуру из conftest.py
def test_jwt_validation_success(create_test_token):
    # Создаем токен с помощью фикстуры
    token = create_test_token(sub="tg_user_123")
    
    # Проверяем валидацию
    payload = decode_and_validate(token)
    assert payload["sub"] == "tg_user_123"

def test_jwt_validation_failure():
    with pytest.raises(ValueError, match="Invalid or expired token"):
        decode_and_validate("not.a.real.token")