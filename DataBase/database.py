from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./todoapp.db'

Engine = create_engine(url=SQL_ALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=Engine)