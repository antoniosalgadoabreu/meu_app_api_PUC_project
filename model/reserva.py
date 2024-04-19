from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Reserva(Base):
    __tablename__ = 'reserva'

    id = Column("pk_reserva", Integer, primary_key=True)
    nome = Column(String(140))
    email = Column(String(140))
    cpf = Column(String(11))
    dataReserva = Column(String(12), unique=True)
    telefone = Column(String(11))
    dataNasc = Column(String(12))
    data_insercao = Column(DateTime, default=datetime.now())    

    def __init__(self, nome:str, email:str, cpf:str, dataReserva: str, 
                 telefone:str, dataNasc:str, data_insercao:Union[DateTime, None] = None):

        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.dataReserva = dataReserva
        self.telefone = telefone
        self.dataNasc = dataNasc
        self.data_insercao = data_insercao


