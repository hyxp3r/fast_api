
from datetime import datetime
import uuid
from sqlalchemy import JSON, Integer, Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Roles(Base):
    __tablename__ = "roles"
    id = Column("id", UUID, primary_key = True, default=uuid.uuid4)
    name = Column("name", String, nullable = False)
    permission = Column("permission", JSON)


class Users(Base):
    __tablename__ = "users"
    id = Column("id", UUID, primary_key = True, default=uuid.uuid4)
    email = Column("email", String, nullable = False)
    username = Column("username", String, nullable = False)
    password = Column("password", String, nullable = False)
    registered_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey("roles.id"))




