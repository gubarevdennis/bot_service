# bot_service/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "bot-service"
    ENV: str = "local" # Добавили, так как в .env есть ENV=local
    TELEGRAM_BOT_TOKEN: str
    
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    
    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    
    # Добавляем эти поля, чтобы Pydantic их не блокировал
    OPENROUTER_SITE_URL: str = "https://example.com"
    OPENROUTER_APP_NAME: str = "bot-service"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()