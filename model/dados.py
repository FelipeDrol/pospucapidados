from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base

class Dados(Base):
    __tablename__ = 'dados'

    id = Column("pk_dados", Integer, primary_key=True)
    json = Column(String(999), nullable=False)
    usuario = Column(String(140), unique=False)
    pagina = Column(String(140), unique=False)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, json:str, usuario:str, pagina:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um registro da pagina de dados para um usuario

        Arguments:
            json: Dados da pagina em formato JSON
            usuario: Nome ou e-mail do usuario logado
            pagina: Pagina a qual o dado pertence
            data_insercao: Data de quando o dado foi inserido à base
        """
        self.json = json
        self.usuario = usuario
        self.pagina = pagina

        if data_insercao:
            self.data_insercao = data_insercao

