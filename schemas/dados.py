from pydantic import BaseModel
from typing import List
from model.dados import Dados

class DadoViewSchema(BaseModel):
    """ 
    Define como um novo dado a ser inserido deve ser representado
    """
    json: str = "{}"
    usuario: str = "usuario@email.com"
    pagina: str = "Dados"

class ListagemDadosSchema(BaseModel):
    """ 
    Define como uma listagem de Dados será retornada
    """
    dados:List[DadoViewSchema]

class DadoEditSchema(BaseModel):
    """ 
    Define como um dado deve ser editado
    """
    json: str = "{}"
    usuario: str = "usuario@email.com"
    pagina: str = "Dados"
    id: int = 1

class DadoBuscaIdSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no id do Dado
    """
    id: int = 1

class DadosBuscaUsuarioSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no usuario e na pagina do Dado
    """
    usuario: str = "usuario@email.com"
    pagina: str = "Dados"

def apresenta_dados(dados: List[Dados]):
    """ 
    Retorna todos os dados
    """
    result = []
    for dado in dados:
        result.append({
            "id": dado.id,
            "usuario": dado.usuario,
            "pagina": dado.pagina,
            "json": dado.json,
            "data_insercao": dado.data_insercao
        })

    return {"dados": result}

def apresenta_dado(dado: Dados):
    """ 
    Retorna um dado
    """
    return {
            "id": dado.id,
            "usuario": dado.usuario,
            "pagina": dado.pagina,
            "json": dado.json,
            "data_insercao": dado.data_insercao
        }