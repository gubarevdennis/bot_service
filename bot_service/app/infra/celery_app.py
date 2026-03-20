# bot_service/app/infra/celery_app.py
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "bot_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
)

# Автоматически ищем задачи в модуле app.tasks
celery_app.autodiscover_tasks(["app.tasks"])