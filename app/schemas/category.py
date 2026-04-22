
from pydantic import BaseModel

from app.schemas.base import BaseResponse 

class CategoryCreate(BaseModel):
    name: str
    
class CategoryUpdate(BaseModel):
    name: str | None = None

class CategoryResponse(BaseResponse):
    name: str
    
