from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    ACTIVIST = "activist"
    ADMIN = "admin"
    MUNICIPALITY = "municipality"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.CITIZEN)
    organization = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    pollution_points = relationship("PollutionPoint", back_populates="creator", foreign_keys="PollutionPoint.user_id")
    confirmed_points = relationship("PollutionPoint", foreign_keys="PollutionPoint.confirmed_by")
    status_changes = relationship("StatusHistory", back_populates="user")
    comments = relationship("Comment", back_populates="user")