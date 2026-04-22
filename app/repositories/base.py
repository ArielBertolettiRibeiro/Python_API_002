import uuid
from typing import List, Optional, Generic, TypeVar, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session
   
    async def create(self, data: dict[str, Any]) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        return instance
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit))
        return result.scalars().all()
        
    async def update(self, instance: ModelType, data: dict) -> ModelType:
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def deactivate(self, instance: ModelType) -> ModelType:
        instance.is_active = False
        await self.session.flush()
        return instance