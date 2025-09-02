from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

from .address import AddressUpdate

class ClientRequest(BaseModel):
    client_name: str
    client_surname: str
    birthday: date
    gender: str
    registration_date: date
    address_id: UUID

class ClientResponse(ClientRequest):
    id: UUID

class ClientUpdate(BaseModel):
    client_name: Optional[str] = Field(None)
    client_surname: Optional[str] = Field(None)
    birthday: Optional[date] = Field(None)
    gender: Optional[str] = Field(None)
    registration_date: Optional[date] = Field(None)
    address: AddressUpdate
