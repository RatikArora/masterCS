from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON, func, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(String(36), primary_key=True)
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    explanation = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    topic = relationship("Topic", back_populates="concepts")

    __table_args__ = (
        Index("ix_concepts_topic_order", "topic_id", "order_index"),
    )
