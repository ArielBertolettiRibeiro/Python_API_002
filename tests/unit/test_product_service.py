import uuid
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.services.product import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import NotFoundException, ConflictException


# ProductService depende de três repositories:
# - product_repository: acesso ao produto
# - category_repository: valida existência da categoria
# - supplier_repository: valida existência do fornecedor


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_category_repository():
    return AsyncMock()


@pytest.fixture
def mock_supplier_repository():
    return AsyncMock()


@pytest.fixture
def service(mock_repository, mock_category_repository, mock_supplier_repository):
    return ProductService(mock_repository, mock_category_repository, mock_supplier_repository)


def make_product_data(**kwargs) -> ProductCreate:
    defaults = dict(
        name="Notebook",
        sku="NB-001",
        price=Decimal("3500.00"),
        min_quantity=2,
        category_id=uuid.uuid4(),
        supplier_id=uuid.uuid4(),
    )
    defaults.update(kwargs)
    return ProductCreate(**defaults)


class TestProductCreate:

    async def test_create_success(self, service, mock_repository, mock_category_repository, mock_supplier_repository):
        mock_product = MagicMock()
        mock_product.name = "Notebook"
        mock_repository.get_by_sku.return_value = None
        mock_category_repository.get_by_id.return_value = MagicMock()
        mock_supplier_repository.get_by_id.return_value = MagicMock()
        mock_repository.create.return_value = mock_product

        data = make_product_data()
        result = await service.create(data)

        mock_repository.get_by_sku.assert_called_once_with(data.sku)
        mock_category_repository.get_by_id.assert_called_once_with(data.category_id)
        mock_supplier_repository.get_by_id.assert_called_once_with(data.supplier_id)
        mock_repository.create.assert_called_once()
        assert result.name == "Notebook"

    async def test_create_raises_conflict_when_sku_already_exists(
        self, service, mock_repository
    ):
        mock_repository.get_by_sku.return_value = MagicMock()

        with pytest.raises(ConflictException):
            await service.create(make_product_data())

        mock_repository.create.assert_not_called()

    async def test_create_raises_not_found_when_category_does_not_exist(
        self, service, mock_repository, mock_category_repository
    ):
        mock_repository.get_by_sku.return_value = None
        mock_category_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.create(make_product_data())

        mock_repository.create.assert_not_called()

    async def test_create_raises_not_found_when_supplier_does_not_exist(
        self, service, mock_repository, mock_category_repository, mock_supplier_repository
    ):
        mock_repository.get_by_sku.return_value = None
        mock_category_repository.get_by_id.return_value = MagicMock()
        mock_supplier_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.create(make_product_data())

        mock_repository.create.assert_not_called()


class TestProductGetById:

    async def test_get_by_id_success(self, service, mock_repository):
        product_id = uuid.uuid4()
        mock_product = MagicMock()
        mock_product.id = product_id
        mock_repository.get_by_id.return_value = mock_product

        result = await service.get_by_id(product_id)

        mock_repository.get_by_id.assert_called_once_with(product_id)
        assert result.id == product_id

    async def test_get_by_id_raises_not_found_when_product_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_id(uuid.uuid4())


class TestProductGetBySku:

    async def test_get_by_sku_success(self, service, mock_repository):
        mock_product = MagicMock()
        mock_product.sku = "NB-001"
        mock_repository.get_by_sku.return_value = mock_product

        result = await service.get_by_sku("NB-001")

        mock_repository.get_by_sku.assert_called_once_with("NB-001")
        assert result.sku == "NB-001"

    async def test_get_by_sku_raises_not_found_when_sku_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_sku.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_sku("INEXISTENTE")


class TestProductGetAll:

    async def test_get_all_returns_list_of_products(self, service, mock_repository):
        mock_repository.get_all.return_value = [MagicMock(), MagicMock()]

        result = await service.get_all()

        assert len(result) == 2
        mock_repository.get_all.assert_called_once()

    async def test_get_all_returns_empty_list_when_no_products_exist(self, service, mock_repository):
        mock_repository.get_all.return_value = []

        result = await service.get_all()

        assert result == []


class TestProductUpdate:

    async def test_update_success(self, service, mock_repository):
        product_id = uuid.uuid4()
        mock_product = MagicMock()
        mock_product.id = product_id
        mock_updated = MagicMock()
        mock_updated.name = "Notebook Pro"

        mock_repository.get_by_id.return_value = mock_product
        mock_repository.update.return_value = mock_updated

        data = ProductUpdate(name="Notebook Pro")
        result = await service.update(product_id, data)

        mock_repository.update.assert_called_once()
        assert result.name == "Notebook Pro"

    async def test_update_raises_not_found_when_product_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.update(uuid.uuid4(), ProductUpdate(name="Qualquer"))

        mock_repository.update.assert_not_called()

    async def test_update_raises_conflict_when_sku_belongs_to_another_product(self, service, mock_repository):
        product_id = uuid.uuid4()

        mock_product = MagicMock()
        mock_product.id = product_id

        mock_sku_conflict = MagicMock()
        mock_sku_conflict.id = uuid.uuid4()  # ID diferente = conflito

        mock_repository.get_by_id.return_value = mock_product
        mock_repository.get_by_sku.return_value = mock_sku_conflict

        with pytest.raises(ConflictException):
            await service.update(product_id, ProductUpdate(sku="SKU-DUPLICADO"))

        mock_repository.update.assert_not_called()

    async def test_update_raises_not_found_when_new_category_does_not_exist(
        self, service, mock_repository, mock_category_repository
    ):
        product_id = uuid.uuid4()
        mock_repository.get_by_id.return_value = MagicMock(id=product_id)
        mock_category_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.update(product_id, ProductUpdate(category_id=uuid.uuid4()))

        mock_repository.update.assert_not_called()

    async def test_update_raises_not_found_when_new_supplier_does_not_exist(
        self, service, mock_repository, mock_supplier_repository
    ):
        product_id = uuid.uuid4()
        mock_repository.get_by_id.return_value = MagicMock(id=product_id)
        mock_supplier_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.update(product_id, ProductUpdate(supplier_id=uuid.uuid4()))

        mock_repository.update.assert_not_called()


class TestProductDeactivate:

    async def test_deactivate_success(self, service, mock_repository):
        product_id = uuid.uuid4()
        mock_product = MagicMock()
        mock_repository.get_by_id.return_value = mock_product

        await service.deactivate(product_id)

        mock_repository.deactivate.assert_called_once_with(mock_product)

    async def test_deactivate_raises_not_found_when_product_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.deactivate(uuid.uuid4())

        mock_repository.deactivate.assert_not_called()


class TestProductGetLowStock:

    async def test_get_low_stock_returns_list_of_products_below_minimum(self, service, mock_repository):
        mock_repository.get_low_stock.return_value = [MagicMock(), MagicMock()]

        result = await service.get_low_stock()

        assert len(result) == 2
        mock_repository.get_low_stock.assert_called_once()

    async def test_get_low_stock_returns_empty_list_when_all_products_are_above_minimum(self, service, mock_repository):
        mock_repository.get_low_stock.return_value = []

        result = await service.get_low_stock()

        assert result == []
