
from datetime import datetime
import uuid
from sqlalchemy import JSON, Boolean, Integer, Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

Base = declarative_base()


class Role(Base):

    __tablename__ = "role"

    id = mapped_column("id", UUID, primary_key = True, default=uuid.uuid4)
    name = mapped_column("name", String, nullable = False)
    permission = mapped_column("permission", JSON)


class User(Base):

    __tablename__ = "user"

    id = mapped_column("id", UUID, primary_key = True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column("username", String, nullable = False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    registered_at = mapped_column("registered_at", TIMESTAMP, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_id: Mapped[UUID] = mapped_column("role_id", UUID, ForeignKey(Role.id, ondelete="CASCADE"))





