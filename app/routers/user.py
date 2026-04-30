import uuid

from fastapi import APIRouter, Depends, Query

from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.depends.services import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.create(data)

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    return await service.get_by_id(user_id)

@router.get("/", response_model=list[UserResponse], status_code=200)
async def get_all(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all(skip=skip, limit=limit)

@router.patch("/{user_id}/deactivate", status_code=204)
async def deactivate_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    await service.deactivate(user_id)

@router.patch("/{user_id}", response_model=UserResponse, status_code=200)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update(user_id, data)