from app.repositories.base import BaseRepository
from app.models.supplier import Supplier
from sqlalchemy import select, or_

class SupplierRepository(BaseRepository[Supplier]):
    model = Supplier

    async def search(self, query: str) -> list[Supplier]:
        term = f"%{query}%"
        result = await self.session.execute(
            select(self.model).where(
                or_(
                    self.model.name.ilike(term),
                    self.model.email.ilike(term),
                    self.model.phone.ilike(term),
                )
            )
        )
        return list(result.scalars().all())