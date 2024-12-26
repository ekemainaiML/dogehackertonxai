from datetime import datetime
import json
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends

from authapi.appwriteservice.appwrite_db import CRUD
from authapi.deps.dependencies import db_dependency
from authapi.models.users_model import UserBase, Token, UserBaseReq, UserStatus, UserBaseRes
from authapi.tables.tables import User
from authapi.utils.utility import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_password_hash, \
    check_user, get_current_user, get_all_users, user_by_email

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

crud = CRUD()


@user_router.post(path="/add_user", status_code=status.HTTP_201_CREATED)
async def add_user(user: UserBaseReq):
    is_user_present = await check_user(
        email = user.username
    )
    if not is_user_present:
        hash_password = get_password_hash(user.password)
        user_data = UserBase(**{"fullname": user.fullname, "username": user.username,
                                "password": str(hash_password), "token": str(hash_password),
                                "signup": True, "loggedin": False,
                                "createdat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "tokenexpires": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        db_user = user_data.model_dump()
        crud.create_user(db_user)
        return user_data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with email {user.username} is already registered')


@user_router.get(path="/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login(username, password):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = create_access_token(
        data={"sub":  str(user['documents'][0]['username']), "password": password},
        expires_delta=access_token_expires)
    crud.update_user(
        username=user['documents'][0]['$id'],
        data={
            'loggedin': True,
            'token': token_data["access_token"],
            'tokenexpires': token_data["access_token_expires"].strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return Token(access_token=token_data["access_token"], token_type="bearer")


@user_router.get(path="/get_user_by_email", status_code=status.HTTP_200_OK, response_model=UserBaseRes,
                 dependencies=[Depends(get_current_user)])
async def get_user_by_email(username: str):
    user = await user_by_email(username)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with {username} not found')
    return user


@user_router.put(path="/update_user_by_email", status_code=status.HTTP_200_OK,
                 dependencies=[Depends(get_current_user)])
async def update_user_by_email(username: str, user: UserBase):
    user_up = await user_by_email(username)
    if user_up is None:
        raise HTTPException(status_code=404, detail='User was not found')
    crud.update_user(
        username=user_up.id,
        data={
            'username': user.username,
            'password': user.password,
            'fullname': user.fullname,
            'signup': user.signup,
            'loggedin': user.loggedin,
        }
    )
    return user_up


@user_router.delete(path="/delete_user_by_email", status_code=status.HTTP_200_OK,
                    dependencies=[Depends(get_current_user)])
async def delete_user_by_email(username: str):
    user = await user_by_email(username)
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    crud.delete_user(username=user.id)


@user_router.get(path="/check_user_status", status_code=status.HTTP_200_OK)
async def check_user_status(username: str):
    user = await user_by_email(username)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with {username} not found')
    return user
