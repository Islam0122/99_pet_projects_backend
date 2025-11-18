from ninja import Schema
from typing import Optional
from datetime import datetime


class UserRegisterSchema(Schema):
    username: str
    password: str
    email: Optional[str] = None


class UserLoginSchema(Schema):
    username: str
    password: str


class UserProfileUpdateSchema(Schema):
    bio: Optional[str] = None
    avatar: Optional[str] = None


class UserSchema(Schema):
    id: int
    username: str
    email: Optional[str] = None


class UserProfileSchema(Schema):
    bio: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserDetailSchema(Schema):
    id: int
    username: str
    email: Optional[str] = None
    profile: Optional[UserProfileSchema] = None


class TokenSchema(Schema):
    access: str
    refresh: str


class CustomTokenSchema(Schema):
    token: str
    user: UserSchema


class MessageSchema(Schema):
    message: str


class ErrorSchema(Schema):
    detail: str