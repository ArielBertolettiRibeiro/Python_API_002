import uuid

from app.models.mixins import TimestampMixin, ActiveMixin

from app.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Uuid


class Supplier(TimestampMixin, ActiveMixin, Base):
    __tablename__="suppliers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4,    
    )

    name: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20), unique=True, nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True,
    )

    products: Mapped[list["Product"]] = relationship(back_populates="supplier", lazy="raise")