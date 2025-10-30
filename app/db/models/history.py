from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from app.db.models.pollution_point import PointStatus


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    point_id = Column(Integer, ForeignKey("pollution_points.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    old_status = Column(SQLEnum(PointStatus))
    new_status = Column(SQLEnum(PointStatus), nullable=False)
    comment = Column(Text)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    point = relationship("PollutionPoint", back_populates="history")
    user = relationship("User", back_populates="status_changes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    point_id = Column(Integer, ForeignKey("pollution_points.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    point = relationship("PollutionPoint", back_populates="comments")
    user = relationship("User", back_populates="comments")