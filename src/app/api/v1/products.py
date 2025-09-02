from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from schemes.product import ProductRequest, ProductResponce, ProductUpdate
from schemes.address import AddressRequest
from schemes.supplier import SupplierRequest
from repositories.product import ProductRepository
from repositories.address import AddressRepository
from repositories.supplier import SupplierRepository
from db.database import get_async_session

product_router = APIRouter()


@product_router.post("/product/", response_model=ProductResponce, status_code=200)
async def add_product(product_data: ProductRequest,
                      address_data: AddressRequest,
                      supplier_data: SupplierRequest,
                      db_session: AsyncSession = Depends(get_async_session)):
    async with db_session.begin():
        address_repo = AddressRepository(db_session=db_session)
        address_dict = address_data.model_dump()
        address = await address_repo.create(address_dict)

        supplier_repo = SupplierRepository(db_session=db_session)
        supplier_dict = supplier_data.model_dump()
        supplier_dict["address_id"] = address.id
        supplier = await supplier_repo.create(supplier_dict)

        product_repo = ProductRepository(db_session=db_session)
        product_dict = product_data.model_dump()
        product_dict["address_id"] = address.id
        product_dict['supplier_id'] = supplier.id
        product_dict['image_id'] = None 
        product = await product_repo.create(product_dict)
        
    return product


@product_router.get("/product/{product_id}", response_model=ProductResponce, status_code=200)
async def get_from_id(product_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepository(db_session=db_session)
    product = await product_repo.get_by_id(id=product_id)
    return product


@product_router.get("/product/", response_model=List[ProductResponce])
async def get_all(
        limit: int = Query(default=10, ge=1), 
        offset: int = Query(default=0, ge=0), 
        db_session: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepository(db_session=db_session)
    request = await product_repo.get_all(limit=limit, offset=offset)
    return request


@product_router.delete("/product/")
async def delet_product(product_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepository(db_session=db_session)
    product = await product_repo.get_by_id(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    

@product_router.patch("/product/", response_model=ProductResponce)
async def update_product(product_id: UUID, 
                         count: int, 
                         update_data: ProductUpdate ,
                         db_session: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepository(db_session=db_session)
    product = await product_repo.get_by_id(id=product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_dict = update_data.model_dump()
    result = product.available_stock - count
    if result < 0:
        raise HTTPException(status_code=404, detail="Недостаточно остатков")
    update_dict['available_stock'] = result
    update_dict['supplier_id'] = product.supplier_id
    update_dict['image_id'] = product.image_id
    update_dict['id'] = product.id
    await product_repo.update(product, update_data=update_dict)
    return update_dict
