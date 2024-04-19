import datetime as dt
from pydantic import BaseModel
from typing import List, Optional
from model.tarefa import Tarefa

class TarefaSchema(BaseModel):
    
    """ Define como uma nova tarefa deve ser inserida
    """
    fk_categoria: int
    descricao: str = "Marcar reunião de teste com a equipe"
    data_prevista: dt.datetime = dt.datetime.now()
    data_inclusao: dt.datetime = dt.datetime.now()
    concluida: bool = False
    descricao_categoria: Optional[str] = None


class TarefaBuscaSchema(BaseModel):
    
    """ Define como deve ser a estrutura que representa a busca. 
        Busca pelo ID ou pela descricao da tarefa.
    """
    id: str
    concluida: bool = False
 

class ListagemTarefasSchema(BaseModel):
    
    """ Define como uma listagem de tarefas será retornada.
    """
    tarefas:List[TarefaSchema]


class TarefaViewSchema(BaseModel):
    
    """ Define como uma tarefa será retornada.
    """
    id: int
    fk_categoria: int
    descricao: str = "Marcar reunião de teste com a equipe"
    data_prevista: dt.datetime = dt.datetime.now()
    data_inclusao: dt.datetime = dt.datetime.now()
    concluida: bool = False
    categoria: str


class TarefaDelSchema(BaseModel):
    
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str
    

class TarefaUpdateSchema(BaseModel):
    
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de atualização. (pode ser incorporada com a TarefaDelSchema em outra versão)
    """
    mensagem: str
    nome: str


def exibe_tarefa(tarefa: Tarefa):
    
    """ Retorna uma representação da tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    return {
        "id": tarefa.id,
        "fk_categoria": tarefa.fk_categoria,
        "descricao": tarefa.descricao,
        "data_prevista": tarefa.data_prevista,
        "data_inclusao": tarefa.data_inclusao,
        "concluida": tarefa.concluida       
    }


def lista_tarefas(tarefas: List[Tarefa]):
    
    """ Retorna uma representação da tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    result = []
    
    for tarefa in tarefas:
        result.append({
            "id": tarefa.id,
            "fk_categoria": tarefa.fk_categoria,
            "descricao": tarefa.descricao,
            "data_prevista": tarefa.data_prevista,
            "data_inclusao": tarefa.data_inclusao,
            "concluida": tarefa.concluida,
            "descricao_categoria": tarefa.categoria.descricao_categoria
        })   
    return {"tarefas": result}

