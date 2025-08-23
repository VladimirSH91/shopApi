from sqlalchemy.ext.asyncio import AsyncSession

from models.address import Address
from .base import BaseRepository

class AddressRepository(BaseRepository):
    def __init__(self,  db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Address)
