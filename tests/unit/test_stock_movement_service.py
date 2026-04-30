import uuid
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, call

from app.services.stock_movement import StockMovementService
from app.schemas.stock_movement import StockMovementCreate
from app.models.enum import MovementType
from app.core.exceptions import NotFoundException, BusinessRuleException


# StockMovementService depende de três repositories:
# - stock_repository: persiste e consulta movimentações
# - product_repository: valida existência e status do produto, atualiza quantidade
# - user_repository: valida existência do usuário


@pytest.fixture
def mock_stock_repository():
    return AsyncMock()


@pytest.fixture
def mock_product_repository():
    return AsyncMock()


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def service(mock_stock_repository, mock_user_repository, mock_product_repository):
    return StockMovementService(mock_stock_repository, mock_user_repository, mock_product_repository)


def make_active_product(quantity: int = 50) -> MagicMock:
    """Cria um mock de produto ativo com quantidade definida."""
    product = MagicMock()
    product.is_active = True
    product.quantity = quantity
    return product


def make_movement_data(
    movement_type: MovementType,
    quantity: int = 10,
    reason: str | None = None,
) -> StockMovementCreate:
    return StockMovementCreate(
        product_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        type=movement_type,
        quantity=quantity,
        reason=reason,
    )


class TestStockMovementRegister:

    async def test_register_entrada_increases_product_quantity(
        self, service, mock_stock_repository, mock_product_repository, mock_user_repository
    ):
        product = make_active_product(quantity=50)
        mock_product_repository.get_by_id.return_value = product
        mock_user_repository.get_by_id.return_value = MagicMock()
        mock_stock_repository.create.return_value = MagicMock()

        data = make_movement_data(MovementType.entrada, quantity=20)
        await service.register(data)

        # Quantidade nova deve ser 50 + 20 = 70
        mock_product_repository.update.assert_called_once_with(product, {"quantity": 70})
        mock_stock_repository.create.assert_called_once()

    async def test_register_saida_decreases_product_quantity(
        self, service, mock_stock_repository, mock_product_repository, mock_user_repository
    ):
        product = make_active_product(quantity=50)
        mock_product_repository.get_by_id.return_value = product
        mock_user_repository.get_by_id.return_value = MagicMock()
        mock_stock_repository.create.return_value = MagicMock()

        data = make_movement_data(MovementType.saida, quantity=20)
        await service.register(data)

        # Quantidade nova deve ser 50 - 20 = 30
        mock_product_repository.update.assert_called_once_with(product, {"quantity": 30})
        mock_stock_repository.create.assert_called_once()

    async def test_register_ajuste_sets_product_quantity_directly(
        self, service, mock_stock_repository, mock_product_repository, mock_user_repository
    ):
        product = make_active_product(quantity=50)
        mock_product_repository.get_by_id.return_value = product
        mock_user_repository.get_by_id.return_value = MagicMock()
        mock_stock_repository.create.return_value = MagicMock()

        data = make_movement_data(MovementType.ajuste, quantity=100, reason="Recontagem física")
        await service.register(data)

        # Ajuste substitui a quantidade pelo valor informado diretamente
        mock_product_repository.update.assert_called_once_with(product, {"quantity": 100})
        mock_stock_repository.create.assert_called_once()

    async def test_register_records_previous_and_new_quantity_in_movement(
        self, service, mock_stock_repository, mock_product_repository, mock_user_repository
    ):
        product = make_active_product(quantity=50)
        mock_product_repository.get_by_id.return_value = product
        mock_user_repository.get_by_id.return_value = MagicMock()
        mock_stock_repository.create.return_value = MagicMock()

        data = make_movement_data(MovementType.entrada, quantity=10)
        await service.register(data)

        create_call_args = mock_stock_repository.create.call_args[0][0]
        assert create_call_args["previous_quantity"] == 50
        assert create_call_args["new_quantity"] == 60

    async def test_register_raises_not_found_when_product_does_not_exist(
        self, service, mock_product_repository
    ):
        mock_product_repository.get_by_id.return_value = None

        data = make_movement_data(MovementType.entrada)

        with pytest.raises(NotFoundException):
            await service.register(data)

        mock_product_repository.update.assert_not_called()
        mock_product_repository.update.assert_not_called()

    async def test_register_raises_business_rule_when_product_is_inactive(
        self, service, mock_product_repository
    ):
        product = MagicMock()
        product.is_active = False
        mock_product_repository.get_by_id.return_value = product

        data = make_movement_data(MovementType.entrada)

        with pytest.raises(BusinessRuleException):
            await service.register(data)

        mock_product_repository.update.assert_not_called()

    async def test_register_raises_not_found_when_user_does_not_exist(
        self, service, mock_product_repository, mock_user_repository
    ):
        mock_product_repository.get_by_id.return_value = make_active_product()
        mock_user_repository.get_by_id.return_value = None

        data = make_movement_data(MovementType.entrada)

        with pytest.raises(NotFoundException):
            await service.register(data)

        mock_product_repository.update.assert_not_called()

    async def test_register_raises_business_rule_when_saida_would_result_in_negative_stock(
        self, service, mock_product_repository, mock_user_repository
    ):
        product = make_active_product(quantity=10)
        mock_product_repository.get_by_id.return_value = product
        mock_user_repository.get_by_id.return_value = MagicMock()

        # Tenta retirar mais do que existe em estoque
        data = make_movement_data(MovementType.saida, quantity=20)

        with pytest.raises(BusinessRuleException):
            await service.register(data)

        mock_product_repository.update.assert_not_called()

    async def test_register_raises_business_rule_when_ajuste_has_no_reason(
        self, service, mock_product_repository, mock_user_repository
    ):
        mock_product_repository.get_by_id.return_value = make_active_product()
        mock_user_repository.get_by_id.return_value = MagicMock()

        # Ajuste sem justificativa
        data = make_movement_data(MovementType.ajuste, quantity=30, reason=None)

        with pytest.raises(BusinessRuleException):
            await service.register(data)

        mock_product_repository.update.assert_not_called()


class TestStockMovementGetById:

    async def test_get_by_id_success(self, service, mock_stock_repository):
        movement_id = uuid.uuid4()
        mock_movement = MagicMock()
        mock_movement.id = movement_id
        mock_stock_repository.get_by_id.return_value = mock_movement

        result = await service.get_by_id(movement_id)

        mock_stock_repository.get_by_id.assert_called_once_with(movement_id)
        assert result.id == movement_id

    async def test_get_by_id_raises_not_found_when_movement_does_not_exist(self, service, mock_stock_repository):
        mock_stock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_id(uuid.uuid4())


class TestStockMovementGetAll:

    async def test_get_all_returns_list_of_movements(self, service, mock_stock_repository):
        mock_stock_repository.get_all.return_value = [MagicMock(), MagicMock()]

        result = await service.get_all()

        assert len(result) == 2
        mock_stock_repository.get_all.assert_called_once()

    async def test_get_all_returns_empty_list_when_no_movements_exist(self, service, mock_stock_repository):
        mock_stock_repository.get_all.return_value = []

        result = await service.get_all()

        assert result == []


class TestStockMovementGetByProduct:

    async def test_get_by_product_success(
        self, service, mock_stock_repository, mock_product_repository
    ):
        product_id = uuid.uuid4()
        mock_product_repository.get_by_id.return_value = MagicMock()
        mock_stock_repository.get_by_product.return_value = [MagicMock(), MagicMock()]

        result = await service.get_by_product(product_id)

        mock_product_repository.get_by_id.assert_called_once_with(product_id)
        mock_stock_repository.get_by_product.assert_called_once_with(product_id)
        assert len(result) == 2

    async def test_get_by_product_raises_not_found_when_product_does_not_exist(
        self, service, mock_stock_repository, mock_product_repository
    ):
        mock_product_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_product(uuid.uuid4())

        mock_stock_repository.get_by_product.assert_not_called()


class TestStockMovementGetByPeriod:

    async def test_get_by_period_returns_movements_within_range(
        self, service, mock_stock_repository
    ):
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        mock_stock_repository.get_by_period.return_value = [MagicMock()]

        result = await service.get_by_period(start, end)

        mock_stock_repository.get_by_period.assert_called_once_with(start, end)
        assert len(result) == 1
