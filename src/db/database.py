from sqlalchemy import create_engine 
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from dotenv import load_dotenv
import os 
 
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_ERROR")

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

session_local = sessionmaker(autoflush=False , autocommit=False , bind=engine)
def get_db():
    try:
        db = session_local()
        yield db 
    finally:
        db.close()
