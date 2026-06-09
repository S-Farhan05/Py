from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQL_ALCHEMY_DATABASE_URL = "sqlite:///./todos.db" # dialect , path to database
engine = create_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False}) 
# connect_args={"check_same_thread": False} -> Only for SQLite , to allow multiple threads to access the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# SQL_ALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# engine = create_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine,)
# Base= declarative_base()

