import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from authapi.appwriteservice.appwrite_db import databases, APPWRITE_DB_ID, APPWRITE_COLLECTION_ID
from authapi.deps.dependencies import db_dependency
from authapi.models.users_model import UserInDB, TokenData, UserBaseRes
from authapi.tables.tables import User
from appwrite.query import Query

logging.getLogger('passlib').setLevel(logging.ERROR)

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme_user = OAuth2PasswordBearer(
    tokenUrl="users/login",
    scheme_name="JWT"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = os.getenv('ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_all_users():
    users = databases.list_documents(
        database_id=APPWRITE_DB_ID,
        collection_id=APPWRITE_COLLECTION_ID,
    )
    return users


async def check_user(email):
    users = await get_all_users()
    if isinstance(users['documents'], list):
        if len(users['documents']) > 0:
            for user in users['documents']:
                if user['username'] == email:
                    return True
    else:
        return False


async def user_by_email(username: str):
    user = databases.list_documents(
        database_id=APPWRITE_DB_ID,
        collection_id=APPWRITE_COLLECTION_ID,
        queries=[Query.equal('username', [username])]
    )

    if user:
        return UserInDB(
            **{"id": user['documents'][0]['$id'],
               "fullname": user['documents'][0]['fullname'],
               "username": user['documents'][0]['username'],
               "password": user['documents'][0]['token'],
               "token": user['documents'][0]['token'],
               "signup": user['documents'][0]['signup'],
               "loggedin": user['documents'][0]['loggedin'],
               "tokenexpires": user['documents'][0]['tokenexpires'],
               "createdat":  user['documents'][0]['createdat']}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {username} is not registered'
        )


async def authenticate_user(username: str, password: str):
    user = databases.list_documents(
        database_id=APPWRITE_DB_ID,
        collection_id=APPWRITE_COLLECTION_ID,
        queries=[Query.equal("username", [username])]
    )

    if not user:
        return False

    verify_pass = verify_password(password, user['documents'][0]['password'])
    if not verify_pass:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "access_token_expires": expire}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme_user)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        password = payload.get("password")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception

    user = await authenticate_user(username=token_data.username, password=password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def binarySearchOnString(arr: list[UserBaseRes], email):
    """
        Perform a binary search on a sorted list of strings to find the target string.

        Parameters:
        arr (list of str): A list of strings to search within.
        target (str): The string to search for.

        Returns:
        int: The index of the target string if found, otherwise -1.
    """
    # Sort the array before performing binary search
    arr.sort()

    left, right = 0, len(arr) - 1
    global target
    while left <= right:
        mid = (left + right) // 2
        mid_val = arr[mid]

        if mid_val.username == email:
            target = [i for i in range(len(arr)) if arr[i].username == email][0]
            print(f'Target: {target}')
            return mid
        elif mid < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def string_to_bytes(string_source: str):
    return bytes(string_source, "utf-8")


def bytes_to_string(bytes_source: bytes):
    return bytes_source.decode("utf-8")
