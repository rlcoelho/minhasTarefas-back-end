from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base

class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column("id_tarefa", Integer, primary_key=True)
    fk_categoria = Column(Integer, ForeignKey("categoria.id_categoria"), nullable=False)
    descricao = Column(String(200))
    data_prevista = Column(DateTime, default=func.now())
    data_inclusao = Column(DateTime, default=func.now())
    concluida = Column(Boolean, default=False)
    categoria = relationship("Categoria")
        
    def __init__(self, fk_categoria: int, descricao:str, data_prevista:Union[DateTime, None] = None,
                 data_inclusao:Union[DateTime, None] = None, concluida:bool = False):
        """
        Cria uma Tarefa

        Arguments:
            fk_categoria: vincula a tarefa a uma categoria
            descricao: descreve a tarefa
            data_prevista: data prevista para realizar a tarefa
            data_inclusao: data de quando a tarefe foi incluida
            concluida: informa se a tarefa está concluída
        """
        self.fk_categoria = fk_categoria
        self.descricao = descricao
        self.data_prevista = data_prevista
        self.data_inclusao = data_inclusao
        self.concluida = concluida

        if data_prevista:
            self.data_prevista = data_prevista
        
        if data_inclusao:
            self.data_inclusao = data_inclusao