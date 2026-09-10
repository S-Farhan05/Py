from fastapi import FastAPI ,Depends, Path ,HTTPException
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

Db_dependency = Annotated[Session,Depends(get_db)]
@app.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db : Db_dependency):
    return db.query(Todos).all()

@app.get('/todo/{todos_id}',status_code=status.HTTP_200_OK)
async def read_todos(db : Db_dependency , todos_id : int = Path(gt=0)):
    todos_model = db.query(Todos).filter(Todos.id == todos_id).first()
    if todos_model is not None:
        return todos_model

    raise HTTPException(status_code=404, detail="Todo Not found")
