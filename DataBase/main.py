from fastapi import FastAPI ,Depends, Path ,HTTPException
from pydantic import BaseModel , Field
from sqlalchemy.orm import Session
import models
from models import Todos
from database import Engine,SessionLocal
from typing import Annotated
from starlette import status

app =FastAPI()

models.Base.metadata.create_all(bind=Engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title : str = Field(min_length=5)
    description : str = Field(min_length=10)
    priority : int =Field(gt=0,lt=6)
    isCompleted : bool

Db_dependency = Annotated[Session,Depends(get_db)]
@app.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db : Db_dependency):
    return db.query(Todos).all()

@app.get('/todos/{todos_id}',status_code=status.HTTP_200_OK)
async def read_todos(db : Db_dependency , todos_id : int = Path(gt=0)):
    todos_model = db.query(Todos).filter(Todos.id == todos_id).first()
    if todos_model is not None:
        return todos_model

    raise HTTPException(status_code=404, detail="Todo Not found")

@app.post('/create_todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db : Db_dependency , todo_request : TodoRequest):
    todo_create = Todos(**todo_request.model_dump())
    db.add(todo_create)
    db.commit()

@app.put('/todos/{todos_id}' ,status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:Db_dependency , todo_request : TodoRequest ,todos_id : int = Path(gt=0)):

    todo_model = db.query(Todos).filter(Todos.id == todos_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404 , detail="The specific id has not been found")

    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.isCompleted = todo_request.isCompleted

    db.add(todo_model)
    db.commit()


@app.delete('/todos/{todos_id}' , status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db :Db_dependency , todos_id : int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todos_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404 ,detail= "Id not found")

    db.query(Todos).filter(Todos.id == todos_id).delete()
    #db.delete(todo_model) cleaner version , Orm checked already , old style sql deletion doing above 
    db.commit()