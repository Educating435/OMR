from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "admin"


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
