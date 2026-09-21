"""SQLAlchemy Database Models Module.

Defines the Object Relational Mapping (ORM) schemas for persistent storage.
"""

from sqlalchemy import Column, Integer, String
from modules.base import Base


class Data(Base):
    """SQLAlchemy model representing the 'data' table.

    Attributes:
        id (int): Primary key unique identifier, auto-incremented.
        text (str): Stored text content, maximum 255 characters.
    """

    __tablename__ = "data"

    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    text = Column(String(255), nullable=False)
