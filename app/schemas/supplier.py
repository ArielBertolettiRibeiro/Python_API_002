from pydantic import BaseModel, EmailStr
from app.schemas.base import BaseResponse

class SupplierCreate(BaseModel):
    name: str
    phone: str | None = None
    email: EmailStr | None = None


class SupplierUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None

class SupplierResponse(BaseResponse):
    name: str
    phone: str | None = None
    email: EmailStr | None = None