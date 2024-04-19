from sqlalchemy import Column, String, Integer

from  model import Base


class Categoria(Base):
    __tablename__ = 'categoria'

    id_categoria = Column(Integer, primary_key=True)
    descricao_categoria = Column(String(50))
    
    def __init__(self, descricao_categoria:str):
        """
        Cria uma Categoria

        Arguments:
            descricao_categoria: descreve a categoria.
        """
        self.descricao_categoria = descricao_categoria

