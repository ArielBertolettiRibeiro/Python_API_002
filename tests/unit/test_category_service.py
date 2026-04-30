import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.category import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.core.exceptions import NotFoundException, ConflictException


# Fluxo padrão de um teste unitário de service:
# 1. Criar o mock do repository
# 2. Definir o que o mock retorna (cenário)
# 3. Instanciar o service com o mock
# 4. Chamar o método
# 5. Verificar o resultado ou exceção esperada


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    return CategoryService(mock_repository)


class TestCategoryCreate:

    async def test_create_success(self, service, mock_repository):
        mock_category = MagicMock()
        mock_category.name = "Eletrônicos"
        mock_repository.get_by_name.return_value = None
        mock_repository.create.return_value = mock_category

        data = CategoryCreate(name="Eletrônicos")
        result = await service.create(data)

        mock_repository.get_by_name.assert_called_once_with("Eletrônicos")
        mock_repository.create.assert_called_once()
        assert result.name == "Eletrônicos"

    async def test_create_raises_conflict_when_name_already_exists(self, service, mock_repository):
        mock_repository.get_by_name.return_value = MagicMock()

        data = CategoryCreate(name="Eletrônicos")

        with pytest.raises(ConflictException):
            await service.create(data)

        # O fluxo deve ser interrompido antes de chegar no repositório
        mock_repository.create.assert_not_called()


class TestCategoryGetById:

    async def test_get_by_id_success(self, service, mock_repository):
        category_id = uuid.uuid4()
        mock_category = MagicMock()
        mock_category.id = category_id
        mock_repository.get_by_id.return_value = mock_category

        result = await service.get_by_id(category_id)

        mock_repository.get_by_id.assert_called_once_with(category_id)
        assert result.id == category_id

    async def test_get_by_id_raises_not_found_when_category_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_id(uuid.uuid4())


class TestCategoryGetAll:

    async def test_get_all_returns_list_of_categories(self, service, mock_repository):
        mock_repository.get_all.return_value = [MagicMock(), MagicMock()]

        result = await service.get_all()

        assert len(result) == 2
        mock_repository.get_all.assert_called_once()

    async def test_get_all_returns_empty_list_when_no_categories_exist(self, service, mock_repository):
        mock_repository.get_all.return_value = []

        result = await service.get_all()

        assert result == []


class TestCategoryUpdate:

    async def test_update_success(self, service, mock_repository):
        category_id = uuid.uuid4()
        mock_category = MagicMock()
        mock_category.id = category_id
        mock_updated = MagicMock()
        mock_updated.name = "Novo Nome"

        mock_repository.get_by_id.return_value = mock_category
        mock_repository.get_by_name.return_value = None
        mock_repository.update.return_value = mock_updated

        data = CategoryUpdate(name="Novo Nome")
        result = await service.update(category_id, data)

        mock_repository.update.assert_called_once()
        assert result.name == "Novo Nome"

    async def test_update_raises_not_found_when_category_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        data = CategoryUpdate(name="Qualquer Nome")

        with pytest.raises(NotFoundException):
            await service.update(uuid.uuid4(), data)

        mock_repository.update.assert_not_called()

    async def test_update_raises_conflict_when_name_belongs_to_another_category(self, service, mock_repository):
        category_id = uuid.uuid4()
        other_id = uuid.uuid4()

        mock_category = MagicMock()
        mock_category.id = category_id

        # Simula que o nome já pertence a OUTRA categoria
        mock_name_conflict = MagicMock()
        mock_name_conflict.id = other_id

        mock_repository.get_by_id.return_value = mock_category
        mock_repository.get_by_name.return_value = mock_name_conflict

        data = CategoryUpdate(name="Nome Duplicado")

        with pytest.raises(ConflictException):
            await service.update(category_id, data)

        mock_repository.update.assert_not_called()

    async def test_update_success_when_name_belongs_to_same_category(self, service, mock_repository):
        category_id = uuid.uuid4()

        mock_category = MagicMock()
        mock_category.id = category_id

        # Simula que get_by_name retornou a MESMA categoria (não é conflito)
        mock_same = MagicMock()
        mock_same.id = category_id

        mock_repository.get_by_id.return_value = mock_category
        mock_repository.get_by_name.return_value = mock_same
        mock_repository.update.return_value = mock_category

        data = CategoryUpdate(name="Mesmo Nome")
        await service.update(category_id, data)

        mock_repository.update.assert_called_once()


class TestCategoryDeactivate:

    async def test_deactivate_success(self, service, mock_repository):
        category_id = uuid.uuid4()
        mock_category = MagicMock()
        mock_repository.get_by_id.return_value = mock_category

        await service.deactivate(category_id)

        mock_repository.deactivate.assert_called_once_with(mock_category)

    async def test_deactivate_raises_not_found_when_category_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.deactivate(uuid.uuid4())

        mock_repository.deactivate.assert_not_called()
