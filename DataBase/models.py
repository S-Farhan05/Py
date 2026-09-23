from database import Base
from sqlalchemy import Column ,String ,Boolean,Integer,ForeignKey
#Data base shape should be in models.py , The api shape should be schema , Like book_request
class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer , primary_key=True,index=True)
    title = Column(String)
    description=Column(String)
    priority =Column(Integer)
    is_completed = Column(Boolean , default=False)
    owner_id = Column(Integer , ForeignKey("users.id"))


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    email = Column(String,unique=True)
    username = Column(String , unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean , default=True)
    role = Column(String)
    phone_number =Column(String) 
    #father_name = Column(String)

    