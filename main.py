from enum import Enum
from typing import Annotated, List, Optional
import uuid
from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field

from auth.manager import get_user_manager
from auth.auth import auth_backend
from auth.database import User
from auth.schemas import UserCreate, UserRead

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title = "Test App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "Ivan"},
    {"id": 3, "role": "trader", "name": "Vasya"},
    {"id": 4, "role": "trader", "name": "Vasya", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]
@app.get("/")
def hello():

    return {"status": 200, "text": "Hello!"}


class DegreeType(Enum):
    
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: str
    type_degree: DegreeType

class User(BaseModel):

    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []

class UserGet(BaseModel):
    status: int = 200
    users: List[User]


@app.get("/users/{user_id}", response_model=UserGet)
def get_user(user_id:int):

    user = [user for user in fake_users if user["id"] == user_id]
    print(user)
    return {"status":200, "users": user}



@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 1):
    return fake_users[offset:][:limit]

@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):

    curent_user = list(filter(lambda user: user.get("id") == user_id, fake_users ))[0]
    curent_user["name"] = new_name
    return {"status": 200, "data": curent_user}


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "buy", "price": 300, "amount": 5.25},
]

class Trade(BaseModel):

    id: int
    user_id: int
    currency: str = Field(max_length = 5)
    side: str
    price: float = Field(ge=0)
    amount: float

@app.post("/trades")
def add_trades(trades: List[Trade]):

    fake_trades.extend(trades)
    return {"status": 200, "data": trades}


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons