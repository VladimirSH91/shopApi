from uuid import UUID
from pydantic import BaseModel

class ImageRequest(BaseModel):
    image: bytes

class ImageResponse(BaseModel):
    id: UUID
