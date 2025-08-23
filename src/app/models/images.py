import uuid
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base


class Images(Base):
    __tablename__ = 'images'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), 
                                          primary_key=True, 
                                          default=uuid.uuid4) 
    image: Mapped[bytes] = mapped_column(BYTEA, nullable=False)

    product = relationship(argument='Product', back_populates='images')
