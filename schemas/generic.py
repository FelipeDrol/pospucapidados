from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """
    Define como uma mensagem de erro será representada
    """
    message: str

class SucessSchema(BaseModel):
    """
    Define como uma mensagem de sucesso será representada
    """
    message: str
