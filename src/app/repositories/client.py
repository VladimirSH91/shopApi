from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .base import BaseRepository
from models.client import Client

class ClientRepository(BaseRepository):
    def __init__(self,  db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Client)

    
    async def get_by_name_and_surname(self, 
                                      name: Optional[str], 
                                      surname: Optional[str]):
        query = select(Client)
        if name:
            query = query.where(Client.client_name == name)
        if surname:
            query = query.where(Client.client_surname == surname)

        result = await self.db_session.execute(query)
        clients = result.scalars().all()
        return clients
