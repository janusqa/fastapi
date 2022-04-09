import email
from pydantic import BaseModel, EmailStr, validator
from datetime import date, datetime
from typing import Optional


class UserBase(BaseModel):
    user_id: int
    email: EmailStr


class UserResponse(UserBase):
    user_created_at: datetime


class User(UserBase):
    password: str
    user_created_at: datetime


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(Post):
    post_id: int
    user_id: int
    post_created_at: datetime
    votes: int
    owner: UserResponse


class InfoResponse(BaseModel):
    detail: str


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    exp: int


class VoteDirectionException(Exception):
    """Custom exception that is raised if vote direction is not a 0 or a 1"""

    def __init__(self, direction: int, message: str) -> None:
        self.direction = direction
        self.message = message
        super().__init__(message)


class VoteRequest(BaseModel):
    post_id: int
    direction: int = 1

    @validator("direction")
    @classmethod
    def direction_valid(cls, direction):
        """Validator to check whether direction is a valid value"""
        if direction < 0 or direction > 1:
            raise VoteDirectionException(
                direction=direction, message="direction should be a 0 or a 1"
            )
        return direction


class VoteResponse(VoteRequest):
    user_id: int
    vote_created_at: datetime
