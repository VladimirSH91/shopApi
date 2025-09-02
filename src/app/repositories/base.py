from typing import Optional
from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class BaseRepository(ABC):
    def __init__(self, db_session: AsyncSession, model):
        self.db_session = db_session
        self.model = model

    async def create(self, data):
        new_md = self.model(**data)
        self.db_session.add(new_md)
        await self.db_session.flush()
        await self.db_session.refresh(new_md)
        return new_md

    async def update(self, data, update_data):
        for key, value in update_data.items():
            setattr(data, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(data)
        return data


    async def delete(self, data) -> None:
        await self.db_session.delete(data)
        await self.db_session.commit()

    async def get_all(self, 
                      limit: Optional[int] = None, 
                      offset: Optional[int] = None):
        
        stmt = select(self.model)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, id: int):
        query = select(self.model).filter(self.model.id == id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_by_filter(self, filter_dict):
        query = select(self.model)
        for attr, value in filter_dict.items():
            query = query.filter(getattr(self.model, attr) == value)
        result = await self.db_session.execute(query)
        return result.scalars().first()
    
