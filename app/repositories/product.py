import uuid
from app.repositories.base import BaseRepository
from app.models.product import Product
from sqlalchemy import select

class ProductRepository(BaseRepository[Product]):
    model = Product

    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.session.execute(select(self.model).where(self.model.sku == sku))
        return result.scalars().first()
    
    async def get_by_category(self, category_id: uuid.UUID) -> list[Product]:
        products = await self.session.execute(
            select(self.model).where(self.model.category_id == category_id)
        ) 
        return list(products.scalars().all())
    
    async def get_by_supplier(self, supplier_id: uuid.UUID) -> list[Product]:
        products = await self.session.execute(
            select(self.model).where(self.model.supplier_id == supplier_id)
        )
        return list(products.scalars().all())
    
    async def get_low_stock(self) -> list[Product]:
        products = await self.session.execute(
            select(self.model).where(self.model.quantity <= self.model.min_quantity, 
                                     self.model.is_active == True
            )
        )
        return list(products.scalars().all())
    
    async def get_all_active(self) -> list[Product]:
        products = await self.session.execute(
            select(self.model).where(self.model.is_active == True)
        )
        return list(products.scalars().all())