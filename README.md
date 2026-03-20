**LLM-Consultation Service**

Распределенная система для LLM-консультаций, состоящая из двух независимых микросервисов:

1. **Auth Service**: Управление пользователями и выдача JWT.
1. **Bot Service**: Telegram-бот с асинхронной обработкой запросов через Celery, RabbitMQ и Redis.

**Архитектура**

- **Auth Service**: FastAPI + SQLite.
- **Bot Service**: Aiogram 3 + Celery (для LLM запросов).
- **Очереди**: RabbitMQ (broker), Redis (result backend / state storage).
-----
**1. Предварительные требования (Локальная установка)**

Для запуска системы в вашей системе должны быть установлены:

1. **Python 3.14+**
1. **uv** (пакетный менеджер)
1. **RabbitMQ** (запущен как сервис)
1. **Redis** (запущен как сервис)

**1.1. Установка и Запуск RabbitMQ и Redis**

Если вы используете macOS, используйте Homebrew для установки и управления службами:

*# Установка, если еще не установлены*

`brew install rabbitmq redis`

*# Запуск служб в фоне*

`brew services start rabbitmq`

`brew services start redis`

**Проверка статуса:**

`brew services list`

*# Убедитесь, что rabbitmq и redis имеют статус "started"*

*(RabbitMQ по умолчанию доступен на порту 5672, Redis на 6379).*

-----
**2. Установка зависимостей**

**Для каждого сервиса (auth\_service/ и bot\_service/)** выполните следующие шаги в отдельном терминале:

*# 1. Перейдите в папку сервиса*

`cd auth\_service`  *# или cd bot\_service*

*# 2. Создайте и активируйте виртуальное окружение*

`uv venv`

`source .venv/bin/activate`

*# 3. Установите зависимости*

`uv sync`

-----
**3. Настройка переменных окружения**

В каждой папке сервиса создайте файл .env и заполните его данными, соответствующими локальному запуску служб:

**В auth\_service/.env:**

`\# ... ваши настройки JWT`

`SQLITE\_PATH=./auth.db`

**В bot\_service/.env:**

`\# ... ваши настройки JWT, OpenRouter`

`REDIS\_URL=redis://localhost:6379/0`

`RABBITMQ\_URL=amqp://guest:guest@localhost:5672//`

-----
**4. Запуск системы**

**Терминал 1: Auth Service**

`cd auth\_service`

`source .venv/bin/activate`

`uv run --active uvicorn main:app --reload --host 0.0.0.0 --port 8000`

*Документация API: [*http://127.0.0.1:8000/docs*](http://127.0.0.1:8000/docs)*

**Терминал 2: Celery Worker (бэкграунд для LLM)**

`cd bot\_service`

`source .venv/bin/activate`

`celery -A app.infra.celery\_app worker --loglevel=info`

**Терминал 3: Bot Service (основной процесс)**

`cd bot\_service`

`source .venv/bin/activate`

*# Запускаем основной модуль, который инициализирует бота*

`uv run --active uvicorn main:app --reload --host 0.0.0.0 --port 8001`

-----
**5. Тестирование**

Для подтверждения инженерных требований выполните тесты:

*# В папке auth\_service:*

`pytest tests/`

*# В папке bot\_service:*

`pytest tests/`

-----
**6. Сценарий работы и подтверждение**

После запуска всех компонентов:

1. **Auth Flow**: Регистрация и получение JWT через Swagger.
![alt text](<images/auth - register 1.png>)
![alt text](<images/auth - register 2.png>)
2. **Telegram Flow**: Авторизация (/token ...) и запрос к боту.
![alt text](<images/auth - login 1.png>)
![alt text](<images/auth - login 2.png>)
3. **Асинхронность**: Проверка наличия сообщений в интерфейсе RabbitMQ Management (доступен на http://localhost:15672).
Очереди
![alt text](<images/rabbit - queues.png>)
Каналы
![alt text](images/rabbit-channels.png)
Подключения
![alt text](<images/rabbit - connections.png>)
4. **Работа celery worker**: Проверка наличия логов
![alt text](<images/celery - log1.png>)
5. **Работа redis**: Проверка наличия token'a
Логи
![alt text](<images/redis - log1.png>)
Вывод токена
![alt text](<images/redis - log2.png>)
6. **Telegram bot**: Проверка корректности отправки сообщений, авторизации и корректности ответов
Авторизация
![alt text](<images/TG 1.png>)
Общение
![alt text](<images/TG 2.png>)
Разлогирование
![alt text](<images/TG 3.png>)
7. **Auth_service**: Проверка корректности логгирования и тестирования сервиса 
Логи
![alt text](<images/auth_service - log.png>)
Тесты
![alt text](<images/bot_service - tests.png>)
8. **Bot_service**: Проверка корректности логгирования и тестирования сервиса 
Логи
![alt text](<images/bot_service - log.png>)
Тесты
![alt text](<images/bot_service - tests.png>)
