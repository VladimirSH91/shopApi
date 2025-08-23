from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from chemes.images import ImagesResponse
from repositories.images import ImagesRepository
from repositories.product import ProductRepository
from db.database import get_async_session

images_router = APIRouter()


@images_router.post("/images/", response_model=ImagesResponse)
async def add_image(product_id: UUID,
                    file: UploadFile = File(...),
                    db_session: AsyncSession = Depends(get_async_session)):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image is empty")

    product_repo = ProductRepository(db_session=db_session)
    product = await product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    image_repo = ImagesRepository(db_session=db_session)
    image = await image_repo.create({"image": image_bytes})

    await product_repo.update(product, {'image_id': image.id})

    return ImagesResponse(id=image.id)



# сюреализация изображений в json почтитать
# s3 хранилище изучить

@images_router.patch('/image/', response_model=ImagesResponse)
async def update_image(image_id: UUID, 
                       file: UploadFile = File(...),
                       db_session: AsyncSession = Depends(get_async_session)):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image is empty")

    image_repo = ImagesRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    await image_repo.update(image, {"image": image_bytes})

    return ImagesResponse(id=image.id)



@images_router.get("/images/", response_model=ImagesResponse)
async def get_image_by_id(image_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    image_repo = ImagesRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return image

@images_router.get("/images/{product_id}", response_model=ImagesResponse)
async def get_product_image_by_id(product_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepository(db_session=db_session)
    product = await product_repo.get_by_id(id=product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Image not found")

    image_id = product.image_id
    image_repo = ImagesRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return image


@images_router.delete("/images/{image_id}")
async def delete_image(image_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    image_repo = ImagesRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    await image_repo.delete(image)
