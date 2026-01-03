from fastapi import FastAPI 
from .db.database import engine, Base
from .db import models # ensure models are imported
from .routes import auth 
app = FastAPI()

Base.metadata.create_all(bind=engine)

app =FastAPI()

app.include_router(auth.router)
