import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.supplier import SupplierService
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.core.exceptions import NotFoundException, ConflictException


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    return SupplierService(mock_repository)


class TestSupplierCreate:

    async def test_create_success(self, service, mock_repository):
        mock_supplier = MagicMock()
        mock_supplier.name = "Fornecedor A"
        mock_repository.get_by_name.return_value = None
        mock_repository.get_by_email.return_value = None
        mock_repository.get_by_phone.return_value = None
        mock_repository.create.return_value = mock_supplier

        data = SupplierCreate(name="Fornecedor A", email="a@a.com", phone="11999990000")
        result = await service.create(data)

        mock_repository.create.assert_called_once()
        assert result.name == "Fornecedor A"

    async def test_create_raises_conflict_when_name_already_exists(self, service, mock_repository):
        mock_repository.get_by_name.return_value = MagicMock()

        data = SupplierCreate(name="Fornecedor A")

        with pytest.raises(ConflictException):
            await service.create(data)

        mock_repository.create.assert_not_called()

    async def test_create_raises_conflict_when_email_already_exists(self, service, mock_repository):
        mock_repository.get_by_name.return_value = None
        mock_repository.get_by_email.return_value = MagicMock()

        data = SupplierCreate(name="Fornecedor Novo", email="duplicado@a.com")

        with pytest.raises(ConflictException):
            await service.create(data)

        mock_repository.create.assert_not_called()

    async def test_create_raises_conflict_when_phone_already_exists(self, service, mock_repository):
        mock_repository.get_by_name.return_value = None
        mock_repository.get_by_email.return_value = None
        mock_repository.get_by_phone.return_value = MagicMock()

        data = SupplierCreate(name="Fornecedor Novo", phone="11999990000")

        with pytest.raises(ConflictException):
            await service.create(data)

        mock_repository.create.assert_not_called()


class TestSupplierGetById:

    async def test_get_by_id_success(self, service, mock_repository):
        supplier_id = uuid.uuid4()
        mock_supplier = MagicMock()
        mock_supplier.id = supplier_id
        mock_repository.get_by_id.return_value = mock_supplier

        result = await service.get_by_id(supplier_id)

        mock_repository.get_by_id.assert_called_once_with(supplier_id)
        assert result.id == supplier_id

    async def test_get_by_id_raises_not_found_when_supplier_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_id(uuid.uuid4())


class TestSupplierGetAll:

    async def test_get_all_returns_list_of_suppliers(self, service, mock_repository):
        mock_repository.get_all.return_value = [MagicMock(), MagicMock()]

        result = await service.get_all()

        assert len(result) == 2
        mock_repository.get_all.assert_called_once()

    async def test_get_all_returns_empty_list_when_no_suppliers_exist(self, service, mock_repository):
        mock_repository.get_all.return_value = []

        result = await service.get_all()

        assert result == []


class TestSupplierUpdate:

    async def test_update_success(self, service, mock_repository):
        supplier_id = uuid.uuid4()
        mock_supplier = MagicMock()
        mock_supplier.id = supplier_id
        mock_updated = MagicMock()
        mock_updated.name = "Novo Nome"

        mock_repository.get_by_id.return_value = mock_supplier
        mock_repository.get_by_name.return_value = None
        mock_repository.update.return_value = mock_updated

        data = SupplierUpdate(name="Novo Nome")
        result = await service.update(supplier_id, data)

        mock_repository.update.assert_called_once()
        assert result.name == "Novo Nome"

    async def test_update_raises_not_found_when_supplier_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.update(uuid.uuid4(), SupplierUpdate(name="Qualquer"))

        mock_repository.update.assert_not_called()

    async def test_update_raises_conflict_when_name_belongs_to_another_supplier(self, service, mock_repository):
        supplier_id = uuid.uuid4()

        mock_supplier = MagicMock()
        mock_supplier.id = supplier_id

        mock_name_conflict = MagicMock()
        mock_name_conflict.id = uuid.uuid4()  # ID diferente = conflito

        mock_repository.get_by_id.return_value = mock_supplier
        mock_repository.get_by_name.return_value = mock_name_conflict

        with pytest.raises(ConflictException):
            await service.update(supplier_id, SupplierUpdate(name="Nome Duplicado"))

        mock_repository.update.assert_not_called()

    async def test_update_raises_conflict_when_email_belongs_to_another_supplier(self, service, mock_repository):
        supplier_id = uuid.uuid4()

        mock_supplier = MagicMock()
        mock_supplier.id = supplier_id

        mock_email_conflict = MagicMock()
        mock_email_conflict.id = uuid.uuid4()

        mock_repository.get_by_id.return_value = mock_supplier
        mock_repository.get_by_name.return_value = None
        mock_repository.get_by_email.return_value = mock_email_conflict

        with pytest.raises(ConflictException):
            await service.update(supplier_id, SupplierUpdate(email="duplicado@a.com"))

        mock_repository.update.assert_not_called()

    async def test_update_raises_conflict_when_phone_belongs_to_another_supplier(self, service, mock_repository):
        supplier_id = uuid.uuid4()

        mock_supplier = MagicMock()
        mock_supplier.id = supplier_id

        mock_phone_conflict = MagicMock()
        mock_phone_conflict.id = uuid.uuid4()

        mock_repository.get_by_id.return_value = mock_supplier
        mock_repository.get_by_name.return_value = None
        mock_repository.get_by_phone.return_value = mock_phone_conflict

        with pytest.raises(ConflictException):
            await service.update(supplier_id, SupplierUpdate(phone="11999990000"))

        mock_repository.update.assert_not_called()


class TestSupplierDeactivate:

    async def test_deactivate_success(self, service, mock_repository):
        supplier_id = uuid.uuid4()
        mock_supplier = MagicMock()
        mock_repository.get_by_id.return_value = mock_supplier

        await service.deactivate(supplier_id)

        mock_repository.deactivate.assert_called_once_with(mock_supplier)

    async def test_deactivate_raises_not_found_when_supplier_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.deactivate(uuid.uuid4())

        mock_repository.deactivate.assert_not_called()
