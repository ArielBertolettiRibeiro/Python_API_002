import uuid
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.core.exceptions import NotFoundException, ConflictException


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create(self, data: CategoryCreate) -> Category:
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise ConflictException("Já existe categoria com esse nome!")
        return await self.repository.create(data.model_dump())
    
    async def get_by_id(self, category_id: uuid.UUID) -> Category:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundException("Categoria não encontrada!")
        return category
    
    async def get_all(self) -> list[Category]:
        return await self.repository.get_all()
    
    async def update(self, category_id: uuid.UUID, data: CategoryUpdate) -> Category:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundException("Categoria não encontrada")
        
        if data.name:
            existing = await self.repository.get_by_name(data.name)
            if existing and existing.id != category_id:
                raise ConflictException("Já existe uma categoria com esse nome!")
            
        return await self.repository.update(category, data.model_dump(exclude_unset=True))
    
    async def deactivate(self, category_id: uuid.UUID) -> None:
        existing = await self.repository.get_by_id(category_id)
        if not existing:
            raise NotFoundException("Categoria não encontrada!")
        await self.repository.deactivate(existing)