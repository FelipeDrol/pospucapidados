from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from model import Session, Dados
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API de Dados", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
dado_tag = Tag(name="Dado", description="Visualização, Adição, edição e remoção de dados à base")

#Metodos Gerais
def get_todos_dados():
    return Session().query(Dados).all()

def retornos_listagem_dados():
    return {"200": ListagemDadosSchema, "400": ErrorSchema, "404": ErrorSchema}

def retornos_dado_view():
    return {"200": DadoViewSchema, "400": ErrorSchema, "404": ErrorSchema}

def retorno_erro(e, mensagem, code):
    logger.warning(e)
    error_msg = mensagem + ": " + repr(e)
    return {"message": error_msg}, code

#Apis Home
@app.get('/', tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')
    
#Apis Dados
@app.get('/dados', tags=[dado_tag], responses = retornos_listagem_dados())
def get_dados():
    """
    Retorna todos os dados cadastrados
    """
    try:
        dados = Session().query(Dados).all()
        return apresenta_dados(dados), 200
    except Exception as e:
        retorno_erro(e, "Não foi possível obter o dado", 400)
        error_msg = "Erro ao buscar todos os dados: " + repr(e)
        return {"message": error_msg}    

@app.get('/dado', tags=[dado_tag], responses = retornos_dado_view())
def get_dado(query: DadosBuscaUsuarioSchema):
    """
    Retorna um Dado a partir do seu usuario e da pagina
    """
    try:
        dado = Session().query(Dados).filter(Dados.usuario == query.usuario, Dados.pagina == query.pagina).first()
        if(dado):
            return apresenta_dado(dado), 200
        else:
            return {"message": "Dado não localizado"}, 404
    except Exception as e:
        retorno_erro(e, "Erro ao obter dado por id", 400)
    
@app.put('/dado', tags=[dado_tag], responses = retornos_dado_view())
def add_dado(form: DadoViewSchema):
    """
    Adiciona um novo dado à base
    Retorna todos os dados cadastrados
    """
    try:
        dado = Dados(json=form.json, usuario = form.usuario, pagina=form.pagina)
        session = Session()
        session.add(dado)
        session.commit()

        return apresenta_dado(dado), 200
    except Exception as e:
        retorno_erro(e, "Não foi possível obter o dado", 400)
        error_msg = "Não foi possível adicionar o novo dado:" + repr(e)
        return {"message": error_msg}

@app.delete('/dado', tags=[dado_tag], responses = retornos_listagem_dados())
def del_dado(query: DadoBuscaIdSchema):
    """
    Deleta um dado a partir do seu id
    Retorna todos os dados cadastrados
    """
    try:
        session = Session()
        sqlQuery = session.query(Dados).filter(Dados.id == query.id)
        dado = sqlQuery.first()
        if(dado):
            sqlQuery.delete()
            session.commit()
            dados = get_todos_dados()
            return apresenta_dados(dados), 200
        else:
            return {"message": "Dado não localizado"}, 404
    except Exception as e:
        retorno_erro(e, "Não foi possível obter o dado")
        error_msg = "Erro ao deletar dado: " + repr(e)
        return {"message": error_msg}, 404
    
@app.post('/dado', tags=[dado_tag], responses = retornos_listagem_dados())
def edit_dado(form: DadoEditSchema):
    """
    Edita um dado existente pelo seu id
    Retorna todos os dados cadastrados
    """
    try:
        session = Session()
        dado = session.query(Dados).filter(Dados.id == form.id).first()
        if(dado):
            dado.json = form.json
            dado.usuario = form.usuario
            dado.pagina = form.pagina
            session.commit()
            dados = get_todos_dados()
            return apresenta_dados(dados), 200
        else:
            return {"message": "Dado não localizado"}, 404
    except Exception as e:
        retorno_erro(e, "Erro ao editar Dado")