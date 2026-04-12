#app_api/modules/connect.py
# creates the connection to PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from modules.base import Base


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app_api/data/data.db")

def get_engine():
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )

def get_session():
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    SessionLocal = get_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# load_dotenv()


# # SQLAlchemy Base class for models
# Base = declarative_base()

# def get_engine():
#     return create_engine(
#         os.getenv("DATABASE_URL"),
#         connect_args={"check_same_thread":False} if "sqlite" in os.getenv("DATABASE_URL", "") else {}
#     )


# def get_session_local():
#     engine = get_engine()
#     return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():
#     """Initialize the SQLite database and ensure required tables exist.

#     Returns: 
#         Session: a new SQLAlchemy sesion bound to the database engine.

#     """
#     SessionLocal = get_session_local()

#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
