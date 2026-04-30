import uuid

from fastapi import APIRouter, Depends, Query

from app.services.product import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.api.depends.services import get_product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return await service.create(data)


@router.get("/low-stock", response_model=list[ProductResponse])
async def list_low_stock(
    service: ProductService = Depends(get_product_service),
):
    return await service.get_low_stock()


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    return await service.get_all(skip=skip, limit=limit)


@router.get("/sku/{sku}", response_model=ProductResponse)
async def get_product_by_sku(
    sku: str,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_sku(sku)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_id(product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return await service.update(product_id, data)


@router.patch("/{product_id}/deactivate", status_code=204)
async def deactivate_product(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    await service.deactivate(product_id)
