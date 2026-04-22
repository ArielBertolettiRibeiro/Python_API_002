import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseResponse(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)