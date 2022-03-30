from fastapi import FastAPI, status
from starlette.responses import RedirectResponse
from routers import plantas, regadores
from database import engine
from models import models

app = FastAPI()
app.include_router(plantas.router)
app.include_router(regadores.router)


@app.get('/')
async def root():
    return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)


models.Base.metadata.create_all(bind=engine)
