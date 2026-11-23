from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base


class WordAnalysis(Base):
    __tablename__ = "word_analyses"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True, nullable=False)
    analysis_result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())