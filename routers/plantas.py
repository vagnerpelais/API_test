from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import models
from utils.get_database import get_database
from utils.exceptions import id_not_found


router = APIRouter(
    prefix='/plantas',
    tags=['plantas'],
    responses={404: {'description': 'Not found'}}
)

'''BASEMODELS'''
class PlantasModel(BaseModel):
    nome: str
    familia: str


class PlantasUpdate(BaseModel):
    nome: Optional[str]
    familia: Optional[str]
    

'''ROUTES'''
@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_plants(db: Session = Depends(get_database)):
    flowers = db.query(models.Planta).all()

    return flowers


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_plant(id: int, db: Session = Depends(get_database)):
    plant_model = db.query(models.Planta).filter(models.Planta.id == id).first()

    if not plant_model:
        return id_not_found()

    return plant_model


@router.post('/', status_code=status.HTTP_201_CREATED)
async def register_plant(planta: PlantasModel, db: Session = Depends(get_database)):
    plant_model = models.Planta()
    plant_model.nome = planta.nome
    plant_model.familia = planta.familia

    db.add(plant_model)
    db.commit()

    return planta


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def delete_plant(id: int, db: Session = Depends(get_database)):
    plant_model = db.query(models.Planta).filter(models.Planta.id == id).first()

    if not plant_model:
        return id_not_found()
    
    db.query(models.Planta).filter(models.Planta.id == id).delete()
    db.commit()

    return {'info': 'planta deletada'}


@router.patch('/editar-planta/{id}', status_code=status.HTTP_200_OK)
async def edit_plant(id: int, plant: PlantasUpdate, db: Session = Depends(get_database)):
    plant_model = db.query(models.Planta).filter(models.Planta.id == id).first()

    if not plant_model:
        return id_not_found()

    if plant.nome:
        plant_model.nome = plant.nome
    if plant.familia:
        plant_model.familia = plant.familia

    db.add(plant_model)
    db.commit()

    return {'info': 'planta atualizada'}
