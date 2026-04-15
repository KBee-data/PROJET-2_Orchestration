# app_api/models/models.py
from sqlalchemy import Column, Integer, String
from modules.base import Base


class Data(Base):
    __tablename__ = "data"

    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    text = Column(String(255), nullable=False)
