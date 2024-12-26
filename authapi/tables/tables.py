from sqlalchemy import Column, Integer, String, Boolean, DateTime, BLOB
from authapi.config.database import Base

image_column_length = 2000000


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), unique=False)
    username = Column(String(50), unique=True)
    password = Column(String(32), unique=True)
    token = Column(String, unique=True)
    signup = Column(Boolean, unique=False)
    loggedin = Column(Boolean, unique=False)
    created_at = Column(DateTime)
    token_expires = Column(DateTime)
