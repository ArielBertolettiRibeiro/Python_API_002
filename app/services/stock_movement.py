import uuid
from datetime import datetime

from app.models.stock_movement import StockMovement
from app.models.enum import MovementType
from app.repositories.stock_movement import StockMovementRepository
from app.repositories.product import ProductRepository
from app.repositories.user import UserRepository
from app.schemas.stock_movement import StockMovementCreate
from app.core.exceptions import NotFoundException, BusinessRuleException

class StockMovementService:
    def __init__(
            self, 
            stock_repository: StockMovementRepository,
            user_repository: UserRepository,
            product_repository: ProductRepository
            ):
        self.stock_repository = stock_repository
        self.user_repository = user_repository
        self.product_repository = product_repository


    async def register(self, data: StockMovementCreate) -> StockMovement:
        product = await self.product_repository.get_by_id(data.product_id)
        if not product:
            raise NotFoundException("Produto não encontrado")
        
        if not product.is_active:
            raise BusinessRuleException("Produto não está ativo")
        
        user = await self.user_repository.get_by_id(data.user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")

        if data.type == MovementType.saida:
            if product.quantity - data.quantity < 0:
                raise BusinessRuleException("Estoque insuficiente para saída")

        if data.type == MovementType.ajuste:
            if not data.reason:
                raise BusinessRuleException("Ajuste exige justificativa")

        previous_quantity = product.quantity

        if data.type == MovementType.entrada:
            new_quantity = product.quantity + data.quantity
        elif data.type == MovementType.saida:
            new_quantity = product.quantity - data.quantity
        else:
            new_quantity = data.quantity

        await self.product_repository.update(product, {"quantity": new_quantity})

        return await self.stock_repository.create({
            "product_id": data.product_id,
            "user_id": data.user_id,
            "type": data.type,
            "quantity": data.quantity,
            "reason": data.reason,
            "previous_quantity": previous_quantity,
            "new_quantity": new_quantity,
        })

    async def get_by_id(self, movement_id: uuid.UUID) -> StockMovement:
        movement = await self.stock_repository.get_by_id(movement_id)
        if not movement:
            raise NotFoundException("Movimentação não encontrada")
        return movement

    async def get_all(self) -> list[StockMovement]:
        return await self.stock_repository.get_all()

    async def get_by_product(self, product_id: uuid.UUID) -> list[StockMovement]:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException("Produto não encontrado")
        return await self.stock_repository.get_by_product(product_id)

    async def get_by_period(self, start: datetime, end: datetime) -> list[StockMovement]:
        return await self.stock_repository.get_by_period(start, end)
