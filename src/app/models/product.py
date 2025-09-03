import uuid
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                          primary_key=True, 
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    available_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    last_update_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    supplier_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('supplier.id'), nullable=False)
    address_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=False) 
    image_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                                ForeignKey('image.id'), nullable=True)

    supplier = relationship(argument='Supplier', back_populates='product')
    image = relationship(argument='Image', back_populates='product')
