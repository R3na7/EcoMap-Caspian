from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    point_id = Column(Integer, ForeignKey("pollution_points.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    point = relationship("PollutionPoint", back_populates="images")