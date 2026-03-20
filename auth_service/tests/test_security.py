import pytest
from datetime import timedelta, datetime, timezone
from app.core.security import create_access_token, decode_token, get_password_hash, verify_password
from app.core.config import settings

# Закомментируем чтение из .env для теста, чтобы использовать константный секрет
settings.JWT_SECRET = "test_secret_key_for_tests" 

def test_password_hashing():
    plain = "my_strong_password"
    hashed = get_password_hash(plain)
    
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong_password", hashed)

def test_jwt_token_creation_and_decoding():
    user_id = 10
    role = "admin"
    
    # Создаем токен
    token = create_access_token(subject=user_id, role=role, expires_delta=timedelta(minutes=5))
    
    # Декодируем и проверяем
    payload = decode_token(token)
    
    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["role"] == role
    # Проверяем, что время жизни установлено (iat и exp будут близки)
    assert "exp" in payload
    assert "iat" in payload

def test_expired_token_decoding():
    # Создаем токен, который истёк (например, 5 минут назад)
    expired_token = create_access_token(
        subject=1, 
        role="user", 
        expires_delta=timedelta(minutes=-5) # Отрицательное время = истекший
    )
    
    payload = decode_token(expired_token)
    assert payload is None