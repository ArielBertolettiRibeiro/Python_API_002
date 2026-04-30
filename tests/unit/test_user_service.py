import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundException, ConflictException


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    return UserService(mock_repository)


class TestUserCreate:

    async def test_create_success(self, service, mock_repository):
        mock_user = MagicMock()
        mock_user.name = "Ariel"
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = mock_user

        data = UserCreate(name="Ariel", email="ariel@email.com", password="senha123")
        result = await service.create(data)

        mock_repository.get_by_email.assert_called_once_with("ariel@email.com")
        mock_repository.create.assert_called_once()
        assert result.name == "Ariel"

    async def test_create_stores_hashed_password_not_plain_text(self, service, mock_repository):
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = MagicMock()

        data = UserCreate(name="Ariel", email="ariel@email.com", password="senha123")
        await service.create(data)

        # Verifica o que foi passado para o repositório
        call_args = mock_repository.create.call_args[0][0]
        assert "hashed_password" in call_args
        assert "password" not in call_args
        # A senha armazenada não pode ser igual ao texto original
        assert call_args["hashed_password"] != "senha123"

    async def test_create_raises_conflict_when_email_already_exists(self, service, mock_repository):
        mock_repository.get_by_email.return_value = MagicMock()

        data = UserCreate(name="Ariel", email="ariel@email.com", password="senha123")

        with pytest.raises(ConflictException):
            await service.create(data)

        mock_repository.create.assert_not_called()


class TestUserGetById:

    async def test_get_by_id_success(self, service, mock_repository):
        user_id = uuid.uuid4()
        mock_user = MagicMock()
        mock_user.id = user_id
        mock_repository.get_by_id.return_value = mock_user

        result = await service.get_by_id(user_id)

        mock_repository.get_by_id.assert_called_once_with(user_id)
        assert result.id == user_id

    async def test_get_by_id_raises_not_found_when_user_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.get_by_id(uuid.uuid4())


class TestUserGetAll:

    async def test_get_all_returns_list_of_users(self, service, mock_repository):
        mock_repository.get_all.return_value = [MagicMock(), MagicMock()]

        result = await service.get_all()

        assert len(result) == 2
        mock_repository.get_all.assert_called_once()

    async def test_get_all_returns_empty_list_when_no_users_exist(self, service, mock_repository):
        mock_repository.get_all.return_value = []

        result = await service.get_all()

        assert result == []


class TestUserUpdate:

    async def test_update_success(self, service, mock_repository):
        user_id = uuid.uuid4()
        mock_user = MagicMock()
        mock_user.id = user_id
        mock_updated = MagicMock()
        mock_updated.name = "Novo Nome"

        mock_repository.get_by_id.return_value = mock_user
        mock_repository.get_by_email.return_value = None
        mock_repository.update.return_value = mock_updated

        data = UserUpdate(name="Novo Nome")
        result = await service.update(user_id, data)

        mock_repository.update.assert_called_once()
        assert result.name == "Novo Nome"

    async def test_update_raises_not_found_when_user_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.update(uuid.uuid4(), UserUpdate(name="Qualquer"))

        mock_repository.update.assert_not_called()

    async def test_update_raises_conflict_when_email_belongs_to_another_user(self, service, mock_repository):
        user_id = uuid.uuid4()

        mock_user = MagicMock()
        mock_user.id = user_id

        mock_email_conflict = MagicMock()
        mock_email_conflict.id = uuid.uuid4()  # ID diferente = conflito

        mock_repository.get_by_id.return_value = mock_user
        mock_repository.get_by_email.return_value = mock_email_conflict

        with pytest.raises(ConflictException):
            await service.update(user_id, UserUpdate(email="duplicado@email.com"))

        mock_repository.update.assert_not_called()

    async def test_update_success_when_email_belongs_to_same_user(self, service, mock_repository):
        user_id = uuid.uuid4()

        mock_user = MagicMock()
        mock_user.id = user_id

        # get_by_email retorna o MESMO usuário — não é conflito
        mock_same = MagicMock()
        mock_same.id = user_id

        mock_repository.get_by_id.return_value = mock_user
        mock_repository.get_by_email.return_value = mock_same
        mock_repository.update.return_value = mock_user

        await service.update(user_id, UserUpdate(email="mesmo@email.com"))

        mock_repository.update.assert_called_once()


class TestUserDeactivate:

    async def test_deactivate_success(self, service, mock_repository):
        user_id = uuid.uuid4()
        mock_user = MagicMock()
        mock_repository.get_by_id.return_value = mock_user

        await service.deactivate(user_id)

        mock_repository.deactivate.assert_called_once_with(mock_user)

    async def test_deactivate_raises_not_found_when_user_does_not_exist(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundException):
            await service.deactivate(uuid.uuid4())

        mock_repository.deactivate.assert_not_called()
