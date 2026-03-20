# auth_service/app/api/routes_auth.py
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_auth_uc, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(
    data: RegisterRequest, 
    uc: AuthUseCase = Depends(get_auth_uc)
):
    # Usecase сам выбросит исключение (например, 409), если пользователь есть
    user = await uc.register(data)
    return UserPublic.model_validate(user)

@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    uc: AuthUseCase = Depends(get_auth_uc)
):
    # Логика логина спрятана в usecase
    token = await uc.login(form_data.username, form_data.password)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    user_id: int = Depends(get_current_user_id),
    uc: AuthUseCase = Depends(get_auth_uc)
):
    return await uc.get_me(user_id)