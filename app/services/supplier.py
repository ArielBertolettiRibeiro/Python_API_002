import uuid

from app.models.supplier import Supplier
from app.repositories.supplier import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.core.exceptions import NotFoundException, ConflictException

class SupplierService:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    async def create(self, data: SupplierCreate) -> Supplier:
        name_existing = await self.repository.get_by_name(data.name)
        if name_existing:
            raise ConflictException("Esse nome já existe")
        
        if data.email:
            existing = await self.repository.get_by_email(data.email)
            if existing:
                raise ConflictException("Email já existe")
            
        if data.phone:
            existing = await self.repository.get_by_phone(data.phone)
            if existing:
                raise ConflictException("Telefone já existe")
            
        return await self.repository.create(data.model_dump())
    
    async def get_by_id(self, supplier_id: uuid.UUID) -> Supplier:
        supplier = await self.repository.get_by_id(supplier_id)
        if not supplier:
            raise NotFoundException("Fornecedor não encontrado")
        return supplier
    
    async def get_all(self) -> list[Supplier]:
        return await self.repository.get_all()
    
    async def update(self, supplier_id: uuid.UUID, data: SupplierUpdate) -> Supplier:
        supplier = await self.repository.get_by_id(supplier_id)
        if not supplier:
            raise NotFoundException("Fornecedor não encontrado")

        if data.name:
            existing = await self.repository.get_by_name(data.name)
            if existing and existing.id != supplier_id:
                raise ConflictException("Nome de fornecedor já existente")
        if data.email:
            existing = await self.repository.get_by_email(data.email)
            if existing and existing.id != supplier_id:
                raise ConflictException("Email de fornecedor já existente")
        if data.phone:
            existing = await self.repository.get_by_phone(data.phone)
            if existing and existing.id != supplier_id:
                raise ConflictException("Telefone de fornecedor já existente")

        return await self.repository.update(supplier, data.model_dump(exclude_unset=True))
    
    async def deactivate(self, supplier_id: uuid.UUID) -> None:
        supplier = await self.repository.get_by_id(supplier_id)
        if not supplier:
            raise NotFoundException("Fornecedor não encontrado")
        
        await self.repository.deactivate(supplier)