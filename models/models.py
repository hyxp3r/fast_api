
from datetime import datetime
from sqlalchemy import JSON, Integer, Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Roles(Base):
    __tablename__ = "roles"
    id = Column("id", Integer, primary_key = True)
    name = Column("name", String, nullable = False)
    permission = Column("permission", JSON)


class Users(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key = True)
    email = Column("email", String, nullable = False)
    username = Column("username", String, nullable = False)
    password = Column("password", String, nullable = False)
    registered_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey("roles.id"))




