from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from models.images import Images

class ImagesRepository(BaseRepository):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Images)
        