from fastapi import Depends
from app.repositories.category import CategoryRepository
from app.api.depends.repositories import get_category_repository
from app.services.category import CategoryService

async def get_category_service(
        repository: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(repository)