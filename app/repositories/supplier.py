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
    
    async def get_by_name(self, name: str) -> Supplier | None:
        result = await self.session.execute(select(self.model).where(self.model.name == name))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Supplier | None:
        result = await self.session.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()

    async def get_by_phone(self, phone: str) -> Supplier | None:
        result = await self.session.execute(select(self.model).where(self.model.phone == phone))
        return result.scalars().first()
