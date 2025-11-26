from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel

from src.services.user_service import CreateUserDTO, UserService, get_user_service
from src.settings import settings

app = FastAPI()


@app.get("/")
async def read_root():
    return settings.model_dump()

class SignUpRequest(BaseModel):
    email: str
    username: str
    full_name: str | None = None

class SignUpResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str | None = None

@app.post("/sign-up")
async def sign_up(
    request: SignUpRequest,
    user_service: Annotated[UserService, Depends(get_user_service)]
    ):
    user_dto = CreateUserDTO(
        email=request.email,
        username=request.username,
        full_name=request.full_name
    )
    try:
        new_user = await user_service.create_user(user_dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return SignUpResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name
    )
