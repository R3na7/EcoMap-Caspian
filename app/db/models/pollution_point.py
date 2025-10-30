from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from geoalchemy2 import Geography
import enum


class PollutionType(str, enum.Enum):
    PLASTIC = "plastic"
    OIL = "oil"
    SEWAGE = "sewage"
    CONSTRUCTION = "construction"
    OTHER = "other"


class PointStatus(str, enum.Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    CLEANED = "cleaned"
    REJECTED = "rejected"


class SeverityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PollutionPoint(Base):
    __tablename__ = "pollution_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # PostGIS Geography для хранения координат
    coordinates = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)

    pollution_type = Column(SQLEnum(PollutionType), nullable=False)
    status = Column(SQLEnum(PointStatus), default=PointStatus.NEW, index=True)
    severity = Column(SQLEnum(SeverityLevel), default=SeverityLevel.MEDIUM)

    description = Column(Text)
    address = Column(String(500))
    region = Column(String(100))

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    confirmed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    confirmed_at = Column(DateTime(timezone=True))

    # Relationships
    creator = relationship("User", back_populates="pollution_points", foreign_keys=[user_id])
    confirmer = relationship("User", foreign_keys=[confirmed_by])
    images = relationship("Image", back_populates="point", cascade="all, delete-orphan")
    history = relationship("StatusHistory", back_populates="point", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="point", cascade="all, delete-orphan")