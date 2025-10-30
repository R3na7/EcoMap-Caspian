from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.db.models.pollution_point import PollutionType, PointStatus, SeverityLevel
from config import settings


class PointCoordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Широта")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота")

    @validator('latitude')
    def validate_caspian_latitude(cls, v):
        if not (settings.CASPIAN_MIN_LAT <= v <= settings.CASPIAN_MAX_LAT):
            raise ValueError(
                f"Координаты вне региона Каспийского моря. Допустимая широта: {settings.CASPIAN_MIN_LAT}-{settings.CASPIAN_MAX_LAT}")
        return v

    @validator('longitude')
    def validate_caspian_longitude(cls, v):
        if not (settings.CASPIAN_MIN_LON <= v <= settings.CASPIAN_MAX_LON):
            raise ValueError(
                f"Координаты вне региона Каспийского моря. Допустимая долгота: {settings.CASPIAN_MIN_LON}-{settings.CASPIAN_MAX_LON}")
        return v


class PollutionPointCreate(BaseModel):
    coordinates: PointCoordinates
    pollution_type: PollutionType
    severity: SeverityLevel = SeverityLevel.MEDIUM
    description: Optional[str] = Field(None, max_length=2000)
    address: Optional[str] = Field(None, max_length=500)
    region: Optional[str] = Field(None, max_length=100)


class PollutionPointUpdate(BaseModel):
    status: Optional[PointStatus] = None
    severity: Optional[SeverityLevel] = None
    description: Optional[str] = None
    comment: Optional[str] = Field(None, description="Комментарий к изменению")


class PollutionPointResponse(BaseModel):
    id: int
    coordinates: PointCoordinates
    pollution_type: PollutionType
    status: PointStatus
    severity: SeverityLevel
    description: Optional[str]
    address: Optional[str]
    region: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    creator_name: Optional[str] = None
    images: List[str] = []

    class Config:
        from_attributes = True


class PollutionPointFilter(BaseModel):
    status: Optional[List[PointStatus]] = None
    pollution_type: Optional[List[PollutionType]] = None
    severity: Optional[List[SeverityLevel]] = None
    region: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lon: Optional[float] = None
    max_lon: Optional[float] = None