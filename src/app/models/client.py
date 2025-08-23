import uuid
from sqlalchemy import String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import date, datetime

from db import Base

class Client(Base):
    __tablename__ = 'client'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                          primary_key=True,
                                          default=uuid.uuid4) 
    client_name: Mapped[str] = mapped_column(String(100), nullable=False) 
    client_surname: Mapped[str] = mapped_column(String(100), nullable=False) 
    birthday: Mapped[date] = mapped_column(Date, nullable=False) 
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False) 
    address_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=False) 

    address = relationship(argument='Address', back_populates='client')
