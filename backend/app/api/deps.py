from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db_session
from app.models import User, UserRole
from app.schemas.common import PaginationParams


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")
DBSession = Annotated[Session, Depends(get_db_session)]


def get_pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)


def get_current_user(db: DBSession, token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        subject = payload.get("sub")
        if not subject or payload.get("type") != "access":
            raise ValueError("invalid token")
    except (JWTError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials") from exc

    user = db.get(User, subject)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(*roles: UserRole):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency


def rate_limit_hook(request: Request) -> None:
    del request
    return None
