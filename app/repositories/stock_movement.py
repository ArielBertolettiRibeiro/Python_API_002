import uuid
from datetime import datetime

from app.repositories.base import BaseRepository
from app.models.stock_movement import StockMovement
from sqlalchemy import select

class StockMovementRepository(BaseRepository[StockMovement]):
    model = StockMovement

    async def get_by_product(self, product_id: uuid.UUID) -> list[StockMovement]:
        result = await self.session.execute(
            select(self.model).where(self.model.product_id == product_id)
        )
        return list(result.scalars().all())

    async def get_by_period(self, start: datetime, end: datetime) -> list[StockMovement]:
        result = await self.session.execute(
            select(self.model).where(
                self.model.created_at >= start,
                self.model.created_at <= end,
            )
        )
        return list(result.scalars().all())
