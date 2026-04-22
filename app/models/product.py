import uuid

from decimal import Decimal

from app.models.mixins import TimestampMixin, ActiveMixin

from app.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Uuid, ForeignKey, Numeric, Integer

class Product(TimestampMixin, ActiveMixin, Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150), nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
    )

    min_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False,
    )
    category: Mapped["Category"] = relationship(back_populates="products", lazy="raise")

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("suppliers.id"), nullable=False,
    )
    supplier: Mapped["Supplier"] = relationship(back_populates="products", lazy="raise")

    stock_movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="product", lazy="raise"
    )
    