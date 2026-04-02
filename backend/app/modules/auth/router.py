from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.schemas import AuthToken, CurrentUserResponse, LoginRequest
from app.modules.auth.service import AuthService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.post("/login", response_model=AuthToken)
def login(payload: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> AuthToken:
    user, access_token = AuthService(db).login(payload.email, payload.password)
    return AuthToken(access_token=access_token, user_id=user.id, role=user.role)


@router.post("/token", response_model=AuthToken)
def token_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> AuthToken:
    user, access_token = AuthService(db).login(form_data.username, form_data.password)
    return AuthToken(access_token=access_token, user_id=user.id, role=user.role)


@router.get("/me", response_model=CurrentUserResponse)
def me(current_user: CurrentUser) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role,
    )
