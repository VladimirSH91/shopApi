import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                          primary_key=True,  
                                          default=uuid.uuid4,
                                          nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False) 
    city: Mapped[str] = mapped_column(String(100), nullable=False) 
    street: Mapped[str] = mapped_column(String(100), nullable=False) 
    
    client = relationship(argument='Client', back_populates='address', cascade='all, delete')
    suppliers = relationship(argument='Supplier', back_populates='address', cascade='all, delete')
