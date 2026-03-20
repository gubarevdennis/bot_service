# auth_service/app/usecases/auth.py
from app.repositories.users import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError
from app.schemas.auth import RegisterRequest
from app.db.models import User

class AuthUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: RegisterRequest) -> User:
        # Проверка: существует ли пользователь?
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsError()
        
        # Хеширование и создание
        hashed = get_password_hash(data.password)
        return await self.repo.create(data.email, hashed)

    async def login(self, email: str, password: str) -> str:
        # Проверка пользователя и пароля
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        # Генерация токена
        return create_access_token(subject=user.id, role=user.role)

    async def get_me(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user