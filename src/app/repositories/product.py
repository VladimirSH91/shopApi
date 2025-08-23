from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from models.product import Product

class ProductRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(model=Product, db_session=db_session)
        