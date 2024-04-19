from pydantic import BaseModel
from typing import List
from model.reserva import Reserva
from datetime import date
from pydantic import BaseModel


class ReservaSchema(BaseModel):
    """ Define como uma nova reserva a ser inserido deve ser representado
    """
    nome: str = "Antonio Luiz"
    email: str = "antonio@gmail.com"
    cpf: str = "111111111111"
    dataReserva: str = "2024-04-30"
    telefone: str = "21111111111"
    dataNasc: str = "1989-11-04"


class ReservaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data de reserva.
    """
    dataReserva: str = "2024-04-30"


class ListagemReservasSchema(BaseModel):
    """ Define como uma listagem de reservas será retornada.
    """
    reserva:List[ReservaSchema]


def apresenta_reservas(reservas: List[Reserva]):
    """ Retorna uma representação do reservas seguindo o schema definido em
        ReservaViewSchema.
    """
    result = []
    for reserva in reservas:
        result.append({
            "nome": reserva.nome,
            "email": reserva.email,
            "cpf": reserva.cpf,
            "dataReserva": reserva.dataReserva,
            "telefone": reserva.telefone,
            "dataNasc": reserva.dataNasc, 
        })

    return {"reservas": result}


class ReservaViewSchema(BaseModel):
    """ Define como uma reserva será retornada: reserva.
    """
    id: int = 1
    nome: str = "Antonio Luiz"
    email: str = "antonio@gmail.com"
    cpf: str = "111111111111"
    dataReserva: str = "2024-04-30"
    telefone: str = "21111111111"
    dataNasc: str = "1989-11-04"


class ReservaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    dataReserva: str

def apresenta_reserva(reserva: Reserva):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {

        "id": reserva.id,
        "nome": reserva.nome,
        "email": reserva.email,
        "cpf": reserva.cpf,
        "dataReserva": reserva.dataReserva,
        "telefone": reserva.telefone,
        "dataNasc": reserva.dataNasc,
    }
