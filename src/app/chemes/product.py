from typing import Optional
from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: str
    category: str
    price: float
    available_stock: int
    last_update_date: date
    supplier_id: UUID
    image_id: Optional[UUID] = Field(None)

class ProductResponce(ProductRequest):
    id: UUID

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
    price: Optional[float] = Field(None)
    available_stock: Optional[int] = Field(None)
    last_update_date: Optional[date] = Field(None)
    supplier_id: Optional[UUID] = Field(None)
    image_id: Optional[UUID] = Field(None)
