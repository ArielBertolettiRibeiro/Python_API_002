from app.repositories.base import BaseRepository
from app.models.category import Category
from sqlalchemy import select

class CategoryRepository(BaseRepository[Category]):
    model = Category

    async def get_by_name(self, name: str) -> Category | None:
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalars().first()