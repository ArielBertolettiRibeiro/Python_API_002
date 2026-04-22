from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_session
from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository
from app.repositories.supplier import SupplierRepository
from app.repositories.user import UserRepository

async def get_category_repository(
    session: AsyncSession = Depends(get_session)
) -> CategoryRepository:
    return CategoryRepository(session)

async def get_supplier_repository(
        session: AsyncSession = Depends(get_session)
) -> SupplierRepository:
    return SupplierRepository(session)

async def get_product_repository(
    session: AsyncSession = Depends(get_session)
) -> ProductRepository:
    return ProductRepository(session)

async def get_user_repository(
    session: AsyncSession = Depends(get_session)
) -> UserRepository:
    return UserRepository(session)