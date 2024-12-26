from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    fullname: str
    username: str
    password: str
    token: str = None
    signup: bool = False
    loggedin: bool = False
    createdat: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tokenexpires: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class UserBaseRes(BaseModel):
    fullname: str
    username: str
    password: str
    token: str = None
    signup: bool = False
    loggedin: bool = False
    createdat: datetime = datetime.utcnow()
    tokenexpires: datetime = datetime.utcnow()


class UserBaseReq(BaseModel):
    fullname: str
    username: str
    password: str


class UserInDB(UserBase):
    id: str
    password: str


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserStatus(BaseModel):
    fullname: str
    username: str
    token: str
    signup: bool
    loggedin: bool
    createdat: str
    tokenexpires: str
    error: str
