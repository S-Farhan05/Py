from sqlalchemy import create_engine ,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool , StaticPool
from router.todos import get_db , get_current_user
from database import Base
from main import app
from fastapi.testclient import TestClient
from fastapi import status 
import pytest
from models import Todos

SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/TestTodoApplicationDatabase'

engine = create_engine(url=SQL_ALCHEMY_DATABASE_URL ,poolclass=QueuePool)
# SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./testtodoapp.db'
# engine = create_engine(url=SQL_ALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False} ,poolclass=StaticPool)

TestSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine)

async def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'Hello' , 'id' : 1 , 'role':'admin'}
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture()
def test_user():

    todos = Todos(
        title = 'Creating fake todos',
        description = 'Making a test todos for testing',
        priority  = 5,
        is_completed = True,
        owner_id = 1
    
    )
    db = TestSessionLocal()
    db.add(todos)
    db.commit()
    yield todos

    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos'))
        connection.commit()


def test_all_todo(test_user):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [

               { 'title' : 'Creating fake todos',
                'description' : 'Making a test todos for testing',
                'priority' : 5,
                'is_completed' : True,
                'owner_id' : 1,
                'id' : 1}    ]