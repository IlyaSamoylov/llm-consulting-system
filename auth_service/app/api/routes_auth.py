from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse, LoginRequest
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUsecase
from app.api.deps import get_auth_uc, get_current_user_id

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, auth_uc: AuthUsecase = Depends(get_auth_uc)) -> UserPublic:
	"""Регистрация пользователя"""
	return await auth_uc.register(data)

@auth_router.post("/login", response_model=TokenResponse)
async def login(
		form: OAuth2PasswordRequestForm = Depends(),
		auth_uc: AuthUsecase = Depends(get_auth_uc)
) -> TokenResponse:
	"""Аутентификация пользователя и выдача JWT-токена"""
	token = await auth_uc.login(LoginRequest(email=form.username, password=form.password))
	return TokenResponse(access_token=token)

@auth_router.get("/me", response_model=UserPublic)
async def me(uid: int = Depends(get_current_user_id),
             auth_uc: AuthUsecase = Depends(get_auth_uc)) -> UserPublic:
	"""Возвращает информацию о текущем пользователе"""
	user = await auth_uc.me(uid=uid)
	return UserPublic.model_validate(user)