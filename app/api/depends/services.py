from fastapi import Depends
from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository
from app.repositories.supplier import SupplierRepository
from app.repositories.user import UserRepository
from app.repositories.stock_movement import StockMovementRepository
from app.api.depends.repositories import get_category_repository, get_product_repository, get_supplier_repository, get_user_repository, get_stock_movement_repository
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService
from app.services.user import UserService
from app.services.stock_movement import StockMovementService

async def get_category_service(
        repository: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(repository)

async def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository),
        category_repository: CategoryRepository = Depends(get_category_repository),
        supplier_repository: SupplierRepository = Depends(get_supplier_repository)
) -> ProductService:
    return ProductService(product_repository, category_repository, supplier_repository)

async def get_supplier_service(
        repository: SupplierRepository = Depends(get_supplier_repository)
) -> SupplierService:
    return SupplierService(repository)

async def get_user_service(
        repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repository)

async def get_stock_movement_service(
        repository: StockMovementRepository = Depends(get_stock_movement_repository)
) -> StockMovementService:
    return StockMovementService(repository)