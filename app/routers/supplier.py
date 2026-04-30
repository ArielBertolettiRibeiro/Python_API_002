import uuid

from fastapi import APIRouter, Depends, Query

from app.services.supplier import SupplierService
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.api.depends.services import get_supplier_service

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post("/", response_model=SupplierResponse, status_code=201)
async def create_supplier(
    data: SupplierCreate,
    service: SupplierService = Depends(get_supplier_service),
):
    return await service.create(data)


@router.get("/", response_model=list[SupplierResponse])
async def list_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: SupplierService = Depends(get_supplier_service),
):
    return await service.get_all(skip=skip, limit=limit)


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: uuid.UUID,
    service: SupplierService = Depends(get_supplier_service),
):
    return await service.get_by_id(supplier_id)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: uuid.UUID,
    data: SupplierUpdate,
    service: SupplierService = Depends(get_supplier_service),
):
    return await service.update(supplier_id, data)


@router.patch("/{supplier_id}/deactivate", status_code=204)
async def deactivate_supplier(
    supplier_id: uuid.UUID,
    service: SupplierService = Depends(get_supplier_service),
):
    await service.deactivate(supplier_id)
