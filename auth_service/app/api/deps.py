# auth_service/app/api/deps.py
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase
from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError

# Фабрика репозитория
async def get_users_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

# Фабрика бизнес-логики (UseCase)
async def get_auth_uc(repo: UserRepository = Depends(get_users_repo)) -> AuthUseCase:
    return AuthUseCase(repo)

# Зависимость для защиты роутов (проверка токена из заголовка Authorization)
async def get_current_user_id(authorization: str = Header(...)) -> int:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise InvalidTokenError()
    
    payload = decode_token(token)
    if not payload:
        raise InvalidTokenError()
    return int(payload["sub"])