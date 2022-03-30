from fastapi import FastAPI
from routers import plantas, regadores
from database import engine
from models import models

app = FastAPI()
app.include_router(plantas.router)
app.include_router(regadores.router)


models.Base.metadata.create_all(bind=engine)
