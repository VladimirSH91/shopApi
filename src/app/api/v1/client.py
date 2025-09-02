from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from schemes.client import ClientRequest, ClientResponse, ClientUpdate
from schemes.address import AddressRequest, AddressResponse
from repositories.client import ClientRepository
from repositories.address import AddressRepository
from db.database import get_async_session

client_router = APIRouter()


# Добавление клиента
@client_router.post("/client/", response_model=ClientResponse, status_code=200)
async def add_client(data: ClientRequest, 
                     address_data: AddressRequest, 
                     db_session: AsyncSession = Depends(get_async_session)):
    
    async with db_session.begin():
        address_repo = AddressRepository(db_session)
        address_dict = address_data.model_dump()
        address = await address_repo.create(address_dict)

        client_repo = ClientRepository(db_session)
        client_dict = data.model_dump()
        client_dict['address_id'] = address.id
        client = await client_repo.create(client_dict)

    return client


# Получение клиентов по имени и фамилии
@client_router.get("/client/search", response_model=List[ClientResponse], status_code=200)
async def get_client_by_name(name: Optional[str]= None, 
                              surname: Optional[str] = None, 
                              db_session: AsyncSession = Depends(get_async_session)):
    client = ClientRepository(db_session)
    result = await client.get_by_name_and_surname(name, surname)
    return result


# Удаление клиента по id
@client_router.delete("/client/{client_id}", status_code=200)
async def delete_client(client_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    client_db = ClientRepository(db_session)
    client = await client_db.get_by_id(client_id)
    if client:
        client_db.delete(client)
    else:
        raise HTTPException(status_code=404, detail="Client not found")


# Получение всех клиентов с пагинацией (limit и offset)
@client_router.get("/client/", response_model=List[ClientResponse], status_code=200)
async def get_all_clients(
    limit: int = Query(default=10, ge=1), 
    offset: int = Query(default=0, ge=0), 
    db_session: AsyncSession = Depends(get_async_session)):

    client = ClientRepository(db_session)
    request = await client.get_all(limit=limit, offset=offset)
    return request


# Изменение адреса клиента
@client_router.patch("/client/{client_id}", 
                     response_model=AddressResponse, 
                     status_code=200)
async def update_client_address(id: UUID, 
                                update_data: ClientUpdate, 
                                db_session: AsyncSession = Depends(get_async_session)):
    client = ClientRepository(db_session=db_session)
    data_client = await client.get_by_id(id) 
    if not data_client:
        raise HTTPException(status_code=404, detail="Client not found")

    address = AddressRepository(db_session=db_session)
    update_dict = update_data.model_dump()
    update_address = await address.create(update_dict['address']) 
    update_dict.pop('address', None)
    update_dict['address_id'] = update_address.id
    await client.update(data_client, update_dict)
    return update_address
