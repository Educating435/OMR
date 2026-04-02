from fastapi import APIRouter, Depends, status

from app.api.deps import DBSession, get_current_user, rate_limit_hook
from app.models import User
from app.repositories.audit_repository import AuditRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse, UserRead
from app.schemas.result import MessageResponse
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", dependencies=[Depends(rate_limit_hook)])


@router.post("/bootstrap-admin", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def bootstrap_admin(payload: LoginRequest, db: DBSession) -> TokenResponse:
    return AuthService(UserRepository(db), AuditRepository(db)).bootstrap_admin(payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DBSession) -> TokenResponse:
    return AuthService(UserRepository(db), AuditRepository(db)).login(payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest, db: DBSession) -> TokenResponse:
    return AuthService(UserRepository(db), AuditRepository(db)).refresh(payload.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(current_user: User = Depends(get_current_user)) -> MessageResponse:
    del current_user
    return MessageResponse(message="Logged out")


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
