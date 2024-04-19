from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Reserva, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
reserva_tag = Tag(name="Reserva", description="Adição, visualização e remoção de reservas à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à uma reserva cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/reserva', tags=[reserva_tag],
          responses={"200": ReservaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_reserva(form: ReservaSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    reserva = Reserva(
        nome = form.nome,
        email = form.email,
        cpf = form.cpf,
        dataReserva = form.dataReserva,
        telefone = form.telefone,
        dataNasc = form.dataNasc,
        )
    logger.debug(f"Adicionando reserva: '{reserva.dataReserva}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(reserva)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado uma reserva na data: '{reserva.dataReserva}'")
        return apresenta_reserva(reserva), 200
    
    except IntegrityError as e:
        # como a duplicidade da data da resera é a provável razão do IntegrityError
        error_msg = "Reserva de mesma data já salva na base :/"
        logger.warning(f"Erro ao adicionar a reserva '{reserva.dataReserva}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar a reserva '{reserva.dataReserva}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/reservas', tags=[reserva_tag],
         responses={"200": ListagemReservasSchema, "404": ErrorSchema})
def get_reservas():
    """Faz a busca por todos as reservas cadastrados

    Retorna uma representação da listagem de reserva.
    """
    logger.debug(f"Coletando reserva ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    reservas = session.query(Reserva).all()

    if not reservas:
        # se não há reserva cadastrados
        return {"reserva": []}, 200
    else:
        logger.debug(f"%d reservas econtradas" % len(reservas))
        # retorna a representação de reserva
        print(reservas)
        return apresenta_reservas(reservas), 200


@app.get('/reserva', tags=[reserva_tag],
         responses={"200": ReservaViewSchema, "404": ErrorSchema})
def get_reserva(query: ReservaBuscaSchema):
    """Faz a busca por um Reserva a partir do id da reserva

    Retorna uma representação dos reservas.
    """
    reserva_id = query.id
    logger.debug(f"Coletando dados sobre a reserva #{reserva_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    reserva = session.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        # se o reserva não foi encontrado
        error_msg = "Reserva não encontrado na base :/"
        logger.warning(f"Erro ao buscar reserva '{reserva_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Reserva econtrada: '{reserva.dataReserva}'")
        # retorna a representação da reserva
        return apresenta_reserva(reserva), 200


@app.delete('/reserva', tags=[reserva_tag],
            responses={"200": ReservaDelSchema, "404": ErrorSchema})
def del_reserva(query: ReservaBuscaSchema):
    """Deleta um Reserva a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    reserva_dataReserva = unquote(unquote(query.dataReserva))
    print(reserva_dataReserva)
    logger.debug(f"Deletando dados sobre reserva #{reserva_dataReserva}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Reserva).filter(Reserva.dataReserva == reserva_dataReserva).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado reserva #{reserva_dataReserva}")
        return {"mesage": "Reserva removido", "id": reserva_dataReserva}
    else:
        # se a reserva não foi encontrado
        error_msg = "Reserva não encontrada na base :/"
        logger.warning(f"Erro ao deletar produto #'{reserva_dataReserva}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": ReservaViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação das reservas e comentários associados.
    """
    reserva_id  = form.reserva_id
    logger.debug(f"Adicionando comentários a reserva #{reserva_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    reserva = session.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        # se produto não encontrado
        error_msg = "Reserva não encontrada na base :/"
        logger.warning(f"Erro ao adicionar comentário a reserva '{reserva_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário a reserva
    reserva.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário a reserva #{reserva_id}")

    # retorna a representação de produto
    return apresenta_reserva(reserva), 200
