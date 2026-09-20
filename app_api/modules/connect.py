"""Database Connection Module.

This module handles database engine initialization and session management
for both SQLite (local development and testing) and PostgreSQL (production).
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app_api/data/data.db")


def get_engine(database_url: str | None = None) -> Engine:
    """Create and return a SQLAlchemy database engine.

    Configures SQLite-specific arguments (such as disabling thread checking)
    if the database URL targets SQLite, or standard arguments for PostgreSQL.

    Args:
        database_url (str | None): Optional connection string. If None,
            defaults to the DATABASE_URL environment variable.

    Returns:
        Engine: Configured SQLAlchemy engine instance.
    """
    url = database_url or os.getenv("DATABASE_URL", DATABASE_URL)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


def get_session(engine: Engine | None = None) -> sessionmaker[Session]:
    """Create and return a configured SQLAlchemy sessionmaker.

    Args:
        engine (Engine | None): Optional SQLAlchemy engine. If None,
            creates an engine via `get_engine()`.

    Returns:
        sessionmaker[Session]: A factory for creating database sessions.
    """
    eng = engine or get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=eng)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session per request.

    Ensures that the database session is always properly closed after
    the request has finished processing.

    Yields:
        Session: Active SQLAlchemy database session.
    """
    session_local = get_session()
    db = session_local()
    try:
        yield db
    finally:
        db.close()
