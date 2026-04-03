#app_api/main.py
from .models.models import Base
from .modules.sqlite_db import engine
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, StringConstraints, Field
from sqlalchemy.orm import Session
from .modules.crud import get_db, input_data, read_db

# Pydantic Models
class TextRequest(BaseModel):
    text : str = Field(min_length=1, description="Enter some text")

class TextResponse(BaseModel):
    id: int
    text : str

#create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/insert")
def insert_text(words:TextRequest, db: Session = Depends(get_db)):
    """Inserts a new text into the database."""
    
    try:
        input_data(db, words.text)
        return {"message": "Text added"}

    except Exception:
        raise HTTPException(status_code=500, detail=f'Database error')
    

@app.get("/read")
def display_data(db: Session = Depends(get_db)):
    """Displays all ids and texts in database."""

    try:
        datab = read_db(db)
        datab = datab.to_dict(orient="records")
        return datab
    except Exception:
        raise HTTPException(status_code=500, detail=f"Database error")

