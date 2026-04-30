import uuid

from fastapi import APIRouter, Depends, Query

from app.services.category import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.api.depends.services import get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.create(data)


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_all(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: uuid.UUID,
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_by_id(category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.update(category_id, data)


@router.patch("/{category_id}/deactivate", status_code=204)
async def deactivate_category(
    category_id: uuid.UUID,
    service: CategoryService = Depends(get_category_service),
):
    await service.deactivate(category_id)
