import uuid

from app.db.base import Base

from app.models.mixins import TimestampMixin, ActiveMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Uuid

class User(TimestampMixin, ActiveMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )

    stock_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="user", lazy="raise",
    )