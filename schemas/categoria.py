from typing import List
from pydantic import BaseModel
from model.categoria import Categoria

class CategoriaSchema(BaseModel):
    
    """ Define como uma nova categoria deve ser inserida
    """
    descricao_categoria: str = "Trabalho"
    

class CategoriaViewSchema(BaseModel):
    
    """ Define como uma categoria será retornada
    """
    id_categoria: int
    descricao_categoria: str = "Trabalho"


class ListagemCategoriasSchema(BaseModel):
    
    """ Define como uma listagem de categorias será retornada.
    """
    categorias:List[CategoriaSchema]
    
    
class CategoriaBuscaSchema(BaseModel):
    
    """ Define como deve ser a estrutura que representa a busca. 
        Busca pelo ID da categoria.
    """
    id_categoria: str


class CategoriaDelSchema(BaseModel):
    
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str
    

class TemTarefasSchema(BaseModel):
    """ Define como deve ser a estrutura que representa se uma categoria tem tarefas associadas. """

    tem_tarefas: bool


def exibe_categoria(categoria: Categoria):
    
    """ Retorna uma representação da categoria seguindo o schema definido em
        CategoriaViewSchema.
    """
    return {
        "id_categoria": categoria.id_categoria,
        "descricao_categoria": categoria.descricao_categoria
    }
    
    
def lista_categorias(categorias: List[Categoria]):
    
    """ Retorna uma representação da categoria seguindo o schema definido em
        CategoriaViewSchema.
    """
    result = []
    
    for categoria in categorias:
        result.append({
            "id_categoria": categoria.id_categoria,
            "descricao_categoria": categoria.descricao_categoria
        })   
    return {"categorias": result}