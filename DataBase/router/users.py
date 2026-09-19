from fastapi import APIRouter ,Depends,HTTPException,status
from models import Todos , Users
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
from .auth import bcrypt_context


router = APIRouter(
    prefix='/user',
    tags=['User'])

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

# all info about user currently loged in
@router.get('/' ,status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401 , detail="User not authorized")

    todo_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
    user_model_info = db.query(Users).filter(Users.id == user.get('id')).first()
    if todo_model or user_model_info is not None:
        return {
            'user_name' : user_model_info.username,
            'first_name' :user_model_info.first_name,
            'last_name':user_model_info.last_name,
            'email':user_model_info.email,

            "todos": [
            {
            "todo_title": todo.title,
             "description": todo.description,
             "priority_level": todo.priority,
             "status_completed": todo.isCompleted,
            }
            for todo in todo_model
                         ],}
        
    return HTTPException(status_code=401 , detail='User Not authorized')

@router.put('/update_password' ,status_code=status.HTTP_204_NO_CONTENT)
async def update_password(db:db_dependency , user:user_dependency , password:str):
    if user is None:
        raise HTTPException(status_code=401 , detail="User not authorized")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404 , detail="User not found")

    hashed_password = bcrypt_context.hash(password)
    user_model.hashed_password = hashed_password
    db.commit()