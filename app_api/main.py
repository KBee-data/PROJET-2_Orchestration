#app_api/main.py
from modules.base import Base
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from modules.connect import get_engine, get_db
from modules.crud import input_data, read_db
from contextlib import asynccontextmanager

# Pydantic Models
class TextRequest(BaseModel):
    text : str = Field(min_length=1, description="Enter some text")

class TextResponse(BaseModel):
    id: int
    text : str

# define lifespan
@asynccontextmanager
async def lifespan(app): 
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/data")
def insert_text(words:TextRequest, db: Session = Depends(get_db)):
    """Inserts a new text into the database."""
    
    try:
        input_data(db, words.text)
        return {"message": "Text added"}

    except Exception:
        raise HTTPException(status_code=500, detail="Database error")
    

@app.get("/data")
def display_data(db: Session = Depends(get_db)):
    """Displays all ids and texts in database."""

    try:
        datab = read_db(db)
        datab = datab.to_dict(orient="records")
        return datab
    
    except Exception as e:
        print("Error:", e)
        raise

    # except Exception:
    #     raise HTTPException(status_code=500, detail=f"Database error")

