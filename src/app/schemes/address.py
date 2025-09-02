from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class AddressRequest(BaseModel):
    country: str
    city: str
    street: str
    

class AddressResponse(AddressRequest):
    id: UUID

class AddressUpdate(BaseModel):
    country: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    street: Optional[str] = Field(None)
