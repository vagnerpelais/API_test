from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import models
from utils.get_database import get_database
from utils.exceptions import id_not_found


router = APIRouter(
    prefix='/regadores',
    tags=['regadores'],
    responses={404: {'description': 'Not found'}}
)

'''BASEMODELS'''
class RegadorModel(BaseModel):
    nome_bomba: str
    alerta_problema: Optional[bool] = False
    realizar_medicao: Optional[bool] = False
    esta_ligada: Optional[bool] = False


class RegadoUpdateModel(BaseModel):
    nome_bomba: Optional[str]
    alerta_problema: Optional[bool] = False
    realizar_medicao: Optional[bool] = False
    esta_ligada: Optional[bool] = False


'''ROUTES'''
@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_watering_cans(db: Session = Depends(get_database)):
    watering_can_model = db.query(models.Regador).all()

    return watering_can_model


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_watering_can(id: int, db: Session = Depends(get_database)):
    watering_can_model = db.query(models.Regador).filter(models.Regador.id == id).first()
    
    if not watering_can_model:
        return id_not_found()


    return watering_can_model


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_watering_can(watering_can: RegadorModel, db: Session = Depends(get_database)):
    watering_can_model = models.Regador()

    watering_can_model.nome_bomba = watering_can.nome_bomba
    watering_can_model.alerta_problema = watering_can.alerta_problema
    watering_can_model.realizar_medicao = watering_can.realizar_medicao
    watering_can_model.esta_ligada = watering_can.esta_ligada

    db.add(watering_can_model)
    db.commit()

    return watering_can


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def delete_watering_can(id: int, db: Session = Depends(get_database)):
    watering_can = db.query(models.Regador).filter(models.Regador.id == id).first()

    if not watering_can:
        return id_not_found()
    
    db.query(models.Regador).filter(models.Regador.id == id).delete()
    db.commit()

    return {'info': 'Regador deletado com sucesso'}


@router.patch('/editar-regador/{id}', status_code=status.HTTP_200_OK)
async def edit_watering_can(id: int, watering_can_model: RegadoUpdateModel, db: Session = Depends(get_database)):
    watering_can = db.query(models.Regador).filter(models.Regador.id == id).first()

    if not watering_can:
        return id_not_found()

    if watering_can_model.nome_bomba:
        watering_can.nome_bomba = watering_can_model.nome_bomba

    if watering_can_model.alerta_problema:
        watering_can.alerta_problema = watering_can_model.alerta_problema

    if watering_can_model.realizar_medicao:
        watering_can.realizar_medicao = watering_can_model.realizar_medicao

    if watering_can_model.esta_ligada:
        watering_can.esta_ligada = watering_can_model.esta_ligada

    db.add(watering_can)
    db.commit()

    return {'info': 'Informações do regador atualizadas'}
