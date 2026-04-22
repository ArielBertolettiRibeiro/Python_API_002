import uuid

from app.models.mixins import TimestampMixin

from app.db.base import Base

from app.models.enum import MovementType 

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum as SAEnum, Integer

class StockMovement(TimestampMixin, Base):
    __tablename__ = "stock_movements"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id"), nullable=False,
    )
    product: Mapped["Product"] = relationship(back_populates="stock_movements", lazy="raise")

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="stock_movements", lazy="raise")

    type: Mapped[MovementType] = mapped_column(
        SAEnum(MovementType), nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
    )

    previous_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )

    new_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )