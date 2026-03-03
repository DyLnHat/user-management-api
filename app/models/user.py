from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

class Role(str, Enum):
    user = "user"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key = True)
    email: str = Field(unique=True, index = True, nullable = False)
    hashed_password: str = Field(nullable = False)
    full_name: str = Field(nullable = False)
    role: Role = Field(default = Role.user)
    is_active: bool = Field(default = True)
    created_at: datetime = Field(default_factory = datetime.utcnow)