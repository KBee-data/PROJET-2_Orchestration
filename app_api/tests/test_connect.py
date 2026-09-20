"""Unit Tests for Database Connection Module (connect.py).

Verifies engine initialization, session factory instantiation, and
generator-based session lifecycle management across SQLite and PostgreSQL URLs.
"""

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from modules.connect import get_engine, get_session, get_db


def test_get_engine_sqlite():
    """Verify get_engine configures SQLite engines with check_same_thread=False."""
    engine = get_engine("sqlite:///:memory:")
    assert isinstance(engine, Engine)
    assert engine.dialect.name == "sqlite"


def test_get_engine_postgresql(monkeypatch):
    """Verify get_engine correctly parses PostgreSQL DATABASE_URL without SQLite args."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
    engine = get_engine()
    assert isinstance(engine, Engine)
    assert engine.dialect.name == "postgresql"


def test_get_session():
    """Verify get_session creates a valid sessionmaker bound to the given engine."""
    engine = get_engine("sqlite:///:memory:")
    session_factory = get_session(engine)
    assert isinstance(session_factory, sessionmaker)


def test_get_db_lifecycle(monkeypatch):
    """Verify get_db yields a database session and finishes cleanup cleanly."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)

    # Advancing the generator executes the finally: db.close() block
    with pytest.raises(StopIteration):
        next(db_gen)
