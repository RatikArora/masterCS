from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, func, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(7), nullable=True)
    order_index = Column(Integer, default=0)
    target_degrees = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    topics = relationship("Topic", back_populates="subject", lazy="selectin")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(String(36), primary_key=True)
    subject_id = Column(String(36), ForeignKey("subjects.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    order_index = Column(Integer, default=0)
    prerequisite_topic_id = Column(String(36), ForeignKey("topics.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    subject = relationship("Subject", back_populates="topics")
    concepts = relationship("Concept", back_populates="topic", lazy="selectin")

    __table_args__ = (
        Index("ix_topics_subject_order", "subject_id", "order_index"),
    )
