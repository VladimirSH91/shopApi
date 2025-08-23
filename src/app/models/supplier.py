import uuid
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base


class Supplier(Base):
    __tablename__ = 'supplier'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                          primary_key=True, 
                                          default=uuid.uuid4) 
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=False)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=False)

    address = relationship(argument='Address', back_populates='suppliers')
    product = relationship(argument='Product', back_populates='supplier')