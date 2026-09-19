from fastapi import APIRouter ,Depends, HTTPException ,Path
from pydantic import BaseModel
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from .auth import get_current_user
from database import SessionLocal
from models import Todos

router= APIRouter(
    prefix='/admin',
    tags =['Admin']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get('/', status_code = status.HTTP_200_OK)
async def get_todos(user:user_dependency ,db:db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401 , detail='User Not Authorized')

    return db.query(Todos).all()

@router.delete('/delete_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo( db:db_dependency,user:user_dependency,todo_id : int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401 , detail="User not authorized")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None :
        raise HTTPException(status_code=404 , detail="Todo have not been found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    