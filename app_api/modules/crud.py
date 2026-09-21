"""Database CRUD Operations Module.

Provides create and read database helper operations for the Text models.
"""

import pandas as pd
from sqlalchemy.orm import Session
from models.models import Data


def input_data(db: Session, text: str) -> Data:
    """Insert a new text record into the database.

    Args:
        db (Session): Active SQLAlchemy database session.
        text (str): The text content to persist.

    Returns:
        Data: The persisted SQLAlchemy model instance with its assigned primary key id.
    """
    item = Data(text=text)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def read_db(db: Session) -> pd.DataFrame:
    """Retrieve all text records from the database as a pandas DataFrame.

    Args:
        db (Session): Active SQLAlchemy database session.

    Returns:
        pd.DataFrame: DataFrame containing 'id' and 'text' columns.
    """
    data = db.query(Data).all()
    data_list = []
    for item in data:
        data_list.append({"id": item.id, "text": item.text})
    df = pd.DataFrame(data_list)
    return df
