from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str


class CurrentUserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str
