from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from chemes.supplier import SupplierRequest, SupplierResponse, SupplierUpdate
from chemes.address import AddressRequest
from repositories.supplier import SupplierRepository
from repositories.address import AddressRepository
from db.database import get_async_session

supplier_router = APIRouter()


@supplier_router.post('/supplier/', response_model=List[SupplierResponse], status_code=200)
async def add_supplier(data: SupplierRequest,
                       address_data: AddressRequest,
                       db_session: AsyncSession = Depends(get_async_session)):
    address_repo = AddressRepository(db_session=db_session)
    address_dict = address_data.model_dump()
    address = await address_repo.create(address_dict)

    supplier_repo = SupplierRepository(db_session=db_session)
    supplier_dict = data.model_dump()
    supplier_dict["address_id"] = address.id
    supplier = await supplier_repo.create(supplier_dict)
    return [supplier]


@supplier_router.delete("/supplier/{supplier_id}")
async def delete(id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    supplier_repo = SupplierRepository(db_session=db_session)
    supplier = await supplier_repo.get_by_id(id)
    if supplier:
        await supplier_repo.delete(supplier)
    else:
        raise HTTPException(status_code=404, detail="Supplier not found")
    

@supplier_router.get("/supplier/{id}", response_model=SupplierResponse)
async def get_by_id(id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    supplier_repo = SupplierRepository(db_session=db_session)

    supplier = await supplier_repo.get_by_id(id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return supplier


@supplier_router.get("/supplier/")
async def get_all(
        limit: int = Query(default=10, ge=1), 
        offset: int = Query(default=0, ge=0), 
        db_session: AsyncSession = Depends(get_async_session)):
    supplier_repo = SupplierRepository(db_session=db_session)
    request = await supplier_repo.get_all(limit=limit, offset=offset)
    return request


@supplier_router.patch("/supplier/{supplier_id}", response_model=AddressRequest, status_code=200)
async def update_supplier_adddress(supplier_id: UUID,
                                   update_data: SupplierUpdate, 
                                   db_session: AsyncSession = Depends(get_async_session)):
    supplier = SupplierRepository(db_session=db_session)

    data_supplier = await supplier.get_by_id(supplier_id)
    if not data_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    address = AddressRepository(db_session=db_session)
    update_dict = update_data.model_dump()
    update_address = await address.create(update_dict['address']) 
    update_dict.pop('address', None)
    update_dict['address_id'] = update_address.id
    await supplier.update(data_supplier, update_dict)
    return update_address
