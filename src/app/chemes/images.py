from uuid import UUID
from pydantic import BaseModel

class ImagesRequest(BaseModel):
    image: bytes

class ImagesResponse(BaseModel):
    id: UUID
