from sqlalchemy.orm import Session
from authapi.config.database import SessionLocal
from typing import Annotated
from fastapi import Depends


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_database)]
