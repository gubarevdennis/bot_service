# bot_service/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "bot-service"
    TELEGRAM_BOT_TOKEN: str
    
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    
    # В docker-compose эти хосты будут резолвиться автоматически
    REDIS_URL: str = "redis://localhost:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"
    
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()