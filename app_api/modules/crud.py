#app_api/modiles/crud.py
import pandas as pd
from .sqlite_db import SessionLocal
from ..models.models import Data


def get_db():
    """Initialize the SQLite database and ensure required tables exist.

    Returns: 
        Session: a new SQLAlchemy sesion bound to the database engine.

    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def input_data(db, text:str):
    item = Data(text=text)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def read_db(db):
    data = db.query(Data).all()
    data_list = []
    for item in data:
        data_list.append({"id":item.id, "text":item.text})
    df = pd.DataFrame(data_list)
    return df

