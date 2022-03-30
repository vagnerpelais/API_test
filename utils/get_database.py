from database import engine, SessionLocal
from models import models


def get_database():
    try:
        db =  SessionLocal()
        yield db
    finally:
        db.close()



models.Base.metadata.create_all(bind=engine)