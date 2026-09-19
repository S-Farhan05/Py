from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from models import Users
from starlette import status
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm ,OAuth2PasswordBearer
from jose import jwt ,JWTError
from datetime import datetime,timedelta,timezone
import secrets

router = APIRouter(prefix="/auth" ,tags=["Authentication"])
bcrypt_context = CryptContext(schemes=['bcrypt'] ,deprecated = 'auto')
OAuth2_Bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


# secret = secrets.token_hex(32)
# print(f"Secret Key: {secret}")
SECRET_KEY = 'a82c2682dc384011fe3b80b68cbf9db5b76575d6dfa97c700b907aae0a166f1c'
ALGORITHM = 'HS256'



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]

def validate_user(username : str , password:str , db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password , user.hashed_password):
        return False

    return user

def create_access_token(username : str , user_id :int, user_role : str, expire_time : timedelta):

    encode = {'sub':username , 'id' :user_id ,'role': user_role}
    expires = datetime.now(timezone.utc) + expire_time
    encode.update({'exp':expires})
    return jwt.encode(encode , SECRET_KEY ,algorithm= ALGORITHM)

async def get_current_user(token :Annotated[str , Depends(OAuth2_Bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username : str = payload.get('sub')
        user_id : id =payload.get('id')
        user_role : str = payload.get('role')
        if user_id is None or username is None:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail="Could not validate credentials")

        return {'username':username ,'id':user_id ,'role': user_role}
    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail="Could not validate credentials")
    

    

# headers , payloads and signature are the three parts of JWT token , signature is used to verify the authenticity of the token and to ensure that it has not been tampered with. The signature is generated using a secret key known only to the server, and it is included in the token along with the header and payload. When a client sends a request with a JWT token, the server can verify the signature using the secret key to ensure that the token is valid and has not been altered.

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

class Token(BaseModel):
    access_token : str
    token_type : str


@router.post("/",status_code=status.HTTP_201_CREATED)
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


@router.post("/token",response_model=Token)
async def Validate_user_by_username_password(form_request : Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):

    user = validate_user(form_request.username,form_request.password,db)

    if not user:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail="Could not validate credentials")
    
    token = create_access_token(user.username , user.id , user.role, timedelta(minutes=30))

    return {'access_token' : token , "token_type" :"Bearer"}