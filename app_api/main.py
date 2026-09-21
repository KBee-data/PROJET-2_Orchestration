"""FastAPI Application Main Entrypoint.

Provides RESTful API endpoints for health monitoring, text ingestion,
and retrieval of persisted records from the database.
"""

from contextlib import asynccontextmanager
from typing import Any
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from modules.base import Base
from modules.connect import get_db, get_engine
from modules.crud import input_data, read_db


class TextRequest(BaseModel):
    """Request payload schema for inserting text.

    Attributes:
        text (str): Non-empty text string to persist.
    """

    text: str = Field(min_length=1, description="Enter some text")


class TextResponse(BaseModel):
    """Response schema representing a persisted text record.

    Attributes:
        id (int): Primary key unique identifier.
        text (str): Persisted text string.
    """

    id: int
    text: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle events.

    On startup, automatically creates all database tables if they do not exist.

    Args:
        app (FastAPI): The running FastAPI application instance.
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SIDORA AI Data API",
    description="Microservice API for text data ingestion and persistence",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", summary="Health Check")
def health_check() -> dict[str, str]:
    """Verify application health and availability.

    Returns:
        dict[str, str]: Status payload confirming the service is active.
    """
    return {"status": "ok"}


@app.post("/data", summary="Insert Text")
def insert_text(words: TextRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    """Insert a new text record into the database.

    Args:
        words (TextRequest): JSON body containing the text string.
        db (Session): Injected database session dependency.

    Returns:
        dict[str, str]: Confirmation message indicating successful persistence.

    Raises:
        HTTPException: HTTP 500 status if an error occurs during database write.
    """
    try:
        input_data(db, words.text)
        return {"message": "Text added"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/data", summary="List All Data")
def display_data(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    """Retrieve all persisted records from the database.

    Args:
        db (Session): Injected database session dependency.

    Returns:
        list[dict[str, Any]]: A list of dictionaries with 'id' and 'text' fields.

    Raises:
        HTTPException: If an error occurs during database read.
    """
    try:
        datab = read_db(db)
        datab_dict = datab.to_dict(orient="records")
        return datab_dict
    except Exception as e:
        print("Error:", e)
        raise
