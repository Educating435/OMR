from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.users.schemas import UserCreate, UserResponse
from app.modules.users.service import UserService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.get("", response_model=list[UserResponse])
def list_users(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[UserResponse]:
    users = UserService(db).list_users()
    return [UserResponse.model_validate(user, from_attributes=True) for user in users]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> UserResponse:
    user = UserService(db).create_user(payload, current_user.id)
    return UserResponse.model_validate(user, from_attributes=True)
