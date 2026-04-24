import uuid
from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundException, ConflictException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, data: UserCreate) -> User:
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise ConflictException("E-mail já cadastrado")

        user_data = data.model_dump(exclude={"password"})
        user_data["hashed_password"] = pwd_context.hash(data.password)

        return await self.repository.create(user_data)

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")
        return user

    async def get_all(self) -> list[User]:
        return await self.repository.get_all()

    async def update(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")

        if data.email:
            existing = await self.repository.get_by_email(data.email)
            if existing and existing.id != user_id:
                raise ConflictException("E-mail já cadastrado")

        return await self.repository.update(user, data.model_dump(exclude_unset=True))

    async def deactivate(self, user_id: uuid.UUID) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")
        await self.repository.deactivate(user)
