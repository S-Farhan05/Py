from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from models import Users
from starlette import status

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
async def create_user(user_request:User_Request):
    # user_request_model=Users(**user_request.model_dump())
    user_request_model = Users(
        email = user_request.email,
        username = user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=user_request.password,
        role=user_request.role,
        is_active= True
        )
    if user_request_model is None:
        raise HTTPException(status_code=500 , detail="Server cant process")

    return user_request

    

