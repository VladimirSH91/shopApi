from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from schemes.image import ImageResponse
from repositories.image import ImageRepository
from repositories.product import ProductRepository
from db.database import get_async_session

image_router = APIRouter()


@image_router.post("/image/", response_model=ImageResponse)
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
    
    image_repo = ImageRepository(db_session=db_session)
    image = await image_repo.create({"image": image_bytes})

    await product_repo.update(product, {'image_id': image.id})

    return ImageResponse(id=image.id)

# сюреализация изображений в json почтитать
# s3 хранилище изучить

@image_router.patch('/image/', response_model=ImageResponse)
async def update_image(image_id: UUID, 
                       file: UploadFile = File(...),
                       db_session: AsyncSession = Depends(get_async_session)):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image is empty")
    
    image_repo = ImageRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    await image_repo.update(image, {"image": image_bytes})

    return ImageResponse(id=image.id)


@image_router.get("/image/", response_model=ImageResponse)
async def get_image_by_id(image_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    image_repo = ImageRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return image

@image_router.get("/image/{product_id}", response_model=ImageResponse)
async def get_product_image_by_id(product_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepository(db_session=db_session)
    product = await product_repo.get_by_id(id=product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Image not found")

    image_id = product.image_id
    image_repo = ImageRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return image


@image_router.delete("/image/{image_id}")
async def delete_image(image_id: UUID, db_session: AsyncSession = Depends(get_async_session)):
    image_repo = ImageRepository(db_session=db_session)
    image = await image_repo.get_by_id(id=image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    await image_repo.delete(image)
