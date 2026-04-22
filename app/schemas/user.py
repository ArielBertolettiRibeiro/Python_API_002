
from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseResponse

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class UserResponse(BaseResponse):
    name: str
    email: EmailStr
    