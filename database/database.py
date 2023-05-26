import json
from fastapi import Depends
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from controllers.sendMail import send_email
# from models.User import User




# Opening JSON file
with open('config.json') as json_file:
    cfg = json.load(json_file)

engine =create_engine(f'mysql+pymysql://{cfg["database"]["user"]}:{cfg["database"]["password"]}@{cfg["database"]["ip"]}:{cfg["database"]["port"]}/{cfg["database"]["dbname"]}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

del cfg

from contextlib import contextmanager
from sqlalchemy.orm import Session
from database.database import engine, Base

# Define your database models here

Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()




