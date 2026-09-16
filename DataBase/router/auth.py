from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from models import Users
from starlette import status
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


bcrypt_context = CryptContext(schemes=['bcrypt'] ,deprecated = 'auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency=Annotated[Session,Depends(get_db)]



router = APIRouter(
)

#     email = Column(String,unique=True)
#     username = Column(String , unique=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     hashed_password = Column(String)
#     is_active = Column(Boolean , default=True)
#     role = Column(String)

class User_Request(BaseModel):
    email : str
    username:str
    first_name:str
    last_name:str
    password:str
    role:str
    # is_active


@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency ,user_request:User_Request):
    # user_request_model=Users(**user_request.model_dump())
    user_request_model = Users(
        email = user_request.email,
        username = user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active= True
        )
    # if user_request_model is None:
    #     raise HTTPException(status_code=500 , detail="Server cant process")

    db.add(user_request_model)
    db.commit()

    

    

