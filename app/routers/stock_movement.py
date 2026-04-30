import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.services.stock_movement import StockMovementService
from app.schemas.stock_movement import StockMovementCreate, StockMovementResponse
from app.api.depends.services import get_stock_movement_service

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.post("/", response_model=StockMovementResponse, status_code=201)
async def register_movement(
    data: StockMovementCreate,
    service: StockMovementService = Depends(get_stock_movement_service),
):
    return await service.register(data)


@router.get("/", response_model=list[StockMovementResponse])
async def list_movements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: StockMovementService = Depends(get_stock_movement_service),
):
    return await service.get_all(skip=skip, limit=limit)


@router.get("/by-period", response_model=list[StockMovementResponse])
async def list_by_period(
    start: datetime = Query(...),
    end: datetime = Query(...),
    service: StockMovementService = Depends(get_stock_movement_service),
):
    return await service.get_by_period(start, end)


@router.get("/by-product/{product_id}", response_model=list[StockMovementResponse])
async def list_by_product(
    product_id: uuid.UUID,
    service: StockMovementService = Depends(get_stock_movement_service),
):
    return await service.get_by_product(product_id)


@router.get("/{movement_id}", response_model=StockMovementResponse)
async def get_movement(
    movement_id: uuid.UUID,
    service: StockMovementService = Depends(get_stock_movement_service),
):
    return await service.get_by_id(movement_id)
