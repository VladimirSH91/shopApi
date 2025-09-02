from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

from .address import AddressUpdate

class SupplierRequest(BaseModel):
    name: str
    address_id: UUID
    phone_number: int


class SupplierResponse(SupplierRequest):
    id: UUID


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None)
    address: AddressUpdate
    phone_number: Optional[int] = Field(None)
