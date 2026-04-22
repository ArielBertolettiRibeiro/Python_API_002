from app.models.user import User
from app.repositories.base import BaseRepository
from sqlalchemy import select

class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalars().first()