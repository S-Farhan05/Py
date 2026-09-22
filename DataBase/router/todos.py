from fastapi import APIRouter ,Depends, Path ,HTTPException
from pydantic import BaseModel , Field
from sqlalchemy.orm import Session
from models import Todos
from database import SessionLocal
from typing import Annotated
from starlette import status
from .auth import get_current_user

router =APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
user_dependency = Annotated[dict,Depends(get_current_user)]
Db_dependency = Annotated[Session,Depends(get_db)]

class TodoRequest(BaseModel):
    title : str = Field(min_length=5)
    description : str = Field(min_length=10)
    priority : int =Field(gt=0,lt=6)
    is_completed  : bool


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(user:user_dependency , db : Db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Not authorized')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get('/todos/{todos_id}',status_code=status.HTTP_200_OK)
async def read_todos(user:user_dependency , db : Db_dependency , todos_id : int = Path(gt=0)):
    if user is None:
            raise HTTPException(status_code=401 , detail = "User not authorized")
    todos_model = db.query(Todos).filter(Todos.id == todos_id).filter(Todos.owner_id == user.get('id')).first()
    if todos_model is not None:
        return todos_model

    raise HTTPException(status_code=404, detail="Todo Not found")

@router.post('/create_todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user : user_dependency , db : Db_dependency , todo_request : TodoRequest):

    if user is None:
        raise HTTPException(status_code=401 , detail = "User not authorized")
    todo_create = Todos(**todo_request.model_dump() , owner_id = user.get('id'))
    db.add(todo_create)
    db.commit()

@router.put('/todos/{todos_id}' ,status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user :user_dependency , db:Db_dependency , todo_request : TodoRequest ,todos_id : int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail = "Not authorized")
    todo_model = db.query(Todos).filter(Todos.id == todos_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404 , detail="The specific id has not been found")

    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.is_completed = todo_request.is_completed

    db.add(todo_model)
    db.commit()


@router.delete('/todos/{todos_id}' , status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency , db :Db_dependency , todos_id : int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404 , detail = "User not authorized")
    todo_model = db.query(Todos).filter(Todos.id == todos_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404 ,detail= "Id not found")

    db.query(Todos).filter(Todos.id == todos_id).filter(Todos.owner_id == user.get('id')).delete()
    #db.delete(todo_model) cleaner version , Orm checked already , old style sql deletion doing above 
    db.commit()