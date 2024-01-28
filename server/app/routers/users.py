from fastapi import APIRouter, Security
from ..utils import VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me(auth_result: str = Security(auth.verify)):
    print(auth_result)
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}