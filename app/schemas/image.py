from pydantic import BaseModel
from datetime import datetime


class ImageResponse(BaseModel):
    id: int
    point_id: int
    file_name: str
    file_size: int
    url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True