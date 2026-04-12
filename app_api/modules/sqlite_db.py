#app_api/modules/sqlite_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.base import Base

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

