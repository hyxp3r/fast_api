from typing import Optional
import uuid

from fastapi_users import schemas, models
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):

    id: uuid.UUID
    email: EmailStr
    username: str
    role_id: uuid.UUID = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):

    username: str
    email: EmailStr
    password: str
    role_id: uuid.UUID = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


