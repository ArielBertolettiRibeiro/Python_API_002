import uuid

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.enum import MovementType

class StockMovementCreate(BaseModel):
    product_id: uuid.UUID
    user_id: uuid.UUID
    type: MovementType
    quantity: int
    reason: str | None = None

class StockMovementResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    user_id: uuid.UUID
    type: MovementType
    quantity: int
    reason: str | None = None
    previous_quantity: int
    new_quantity: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
