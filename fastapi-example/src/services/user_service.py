from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models.user import User

class CreateUserDTO(BaseModel):
    email: str
    username: str
    full_name: str | None = None

class UserDTO(BaseModel):
    id: int
    email: str
    username: str
    full_name: str | None = None

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def create_user(self, user_dto: CreateUserDTO) -> UserDTO:
        new_user = User(
            email=user_dto.email,
            username=user_dto.username,
            full_name=user_dto.full_name
        )
        self.db_session.add(new_user)
        try:
            await self.db_session.commit()
        except IntegrityError as e:
            await self.db_session.rollback()
            raise ValueError("User with given email or username already exists") from e
        
        await self.db_session.refresh(new_user)
        return UserDTO(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            full_name=new_user.full_name
        )

    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        user = await self.db_session.get(User, user_id)
        if user is None:
            return None
        return UserDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name
        )


def get_user_service(
        db_session: Annotated[AsyncSession, Depends(get_db)]
    ) -> UserService:
    return UserService(db_session)
