import uuid
from decimal import Decimal
from pydantic import BaseModel
from app.schemas.base import BaseResponse

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str | None = None
    price: Decimal
    min_quantity: int
    category_id: uuid.UUID
    supplier_id: uuid.UUID

class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    description: str | None = None
    price: Decimal | None = None
    min_quantity: int | None = None
    category_id: uuid.UUID | None = None
    supplier_id: uuid.UUID | None = None

class ProductResponse(BaseResponse):
    name: str
    sku: str
    description: str | None = None
    price: Decimal
    quantity: int
    min_quantity: int
    category_id: uuid.UUID
    supplier_id: uuid.UUID
