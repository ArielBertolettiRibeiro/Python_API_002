import uuid

from app.models.product import Product
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from app.repositories.supplier import SupplierRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import NotFoundException, ConflictException

class ProductService:
    def __init__(
            self, 
            repository: ProductRepository,
            category_repository: CategoryRepository,
            supplier_repository: SupplierRepository):
        self.repository = repository
        self.category_repository = category_repository
        self.supplier_repository = supplier_repository

    async def create(self, data: ProductCreate) -> Product:
        
        sku = await self.repository.get_by_sku(data.sku)
        if sku:
            raise ConflictException("SKU já existe")
        
        category = await self.category_repository.get_by_id(data.category_id)
        if not category:
            raise NotFoundException("Categoria deve existir")
        
        supplier = await self.supplier_repository.get_by_id(data.supplier_id)
        if not supplier:
            raise NotFoundException("Fornecedor deve existir")
        
        return await self.repository.create(data.model_dump())
    
    async def get_by_id(self, product_id: uuid.UUID) -> Product:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise NotFoundException("Produto não encontrado")
        return product
    
    async def get_by_sku(self, sku: str) -> Product:
        product_sku = await self.repository.get_by_sku(sku)
        if not product_sku:
            raise NotFoundException("SKU específico não encontrado")
        return product_sku
    
    async def get_all(self) -> list[Product]:
        return await self.repository.get_all()
    
    async def deactivate(self, product_id: uuid.UUID) -> None:

        product = await self.repository.get_by_id(product_id)
        if not product:
            raise NotFoundException("Produto não encontrado")
        await self.repository.deactivate(product)
    
    async def update(self, product_id: uuid.UUID, data: ProductUpdate) -> Product:

        product = await self.repository.get_by_id(product_id)
        if not product:
            raise NotFoundException("Produto não encontrado")
        
        if data.sku:
            existing = await self.repository.get_by_sku(data.sku)
            if existing and existing.id != product_id:
                raise ConflictException("SKU já existe")
            
        if data.category_id:
            category = await self.category_repository.get_by_id(data.category_id)
            if not category:
                raise NotFoundException("Categoria deve existir")
            
        if data.supplier_id:
            supplier = await self.supplier_repository.get_by_id(data.supplier_id)
            if not supplier:
                raise NotFoundException("Fornecedor deve existir")
            
        return await self.repository.update(product, data.model_dump(exclude_unset=True))

    async def get_low_stock(self) -> list[Product]:
        return await self.repository.get_low_stock()

        
        
        
