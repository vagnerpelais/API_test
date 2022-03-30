from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Planta(Base):
    __tablename__ = 'planta'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    familia = Column(String)


class Regador(Base):
    __tablename__ = 'regador'

    id = Column(Integer, primary_key=True, index=True)
    nome_bomba = Column(String)
    alerta_problema = Column(Boolean, default=False)
    realizar_medicao = Column(Boolean, default=True)
    esta_ligada = Column(Boolean, default=False)
