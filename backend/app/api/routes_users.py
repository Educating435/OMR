from fastapi import APIRouter, Depends, status

from app.api.deps import DBSession, get_current_user, require_roles
from app.models import User, UserRole
from app.repositories.audit_repository import AuditRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, UserRead
from app.services.auth_service import AuthService


router = APIRouter(prefix="")


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/users", response_model=list[UserRead])
def list_users(
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> list[User]:
    del current_user
    return UserRepository(db).list()


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> User:
    del current_user
    return AuthService(UserRepository(db), AuditRepository(db)).create_user(payload)
