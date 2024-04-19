from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from model import Session, Tarefa, Categoria
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minhas Tarefas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc.")
tarefa_tag = Tag(name="Tarefa", description="Inclusão, visualização e remoção de tarefas.")
categoria_tag = Tag(name="Categoria", description="Inclusão, visualização e desativação de categorias.")


@app.get('/', tags=[home_tag])
def home():    
    
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/tarefa/', tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa(form: TarefaSchema):
    
    """Adiciona uma nova tarefa.
    """
        
    tarefa = Tarefa(
        fk_categoria=form.fk_categoria,
        descricao=form.descricao,
        data_prevista=form.data_prevista,
        data_inclusao=form.data_inclusao,
        concluida = False
        )
    
    logger.debug(f"Adicionando tarefa: '{tarefa.descricao}'")
    
    try:
        # cria conexão com a base e adiciona a tarefa
        session = Session()
        session.add(tarefa)
        session.commit()
        
        logger.debug(f"Adicionado tarefa: '{tarefa.descricao}'")
        
        return exibe_tarefa(tarefa), 200

    except IntegrityError as e:
        # erro de integridade do IntegrityError
        error_msg = "Erro de integridade:/"
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.descricao}', {error_msg}")
        
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova tarefa:/"
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.descricao}', {error_msg}")
        
        return {"mensagem": error_msg}, 400


@app.get('/tarefas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas():
    """Lista todas as tarefas cadastradas.

    Retorna uma representação da listagem de tarefas.
    """
    logger.debug(f"Coletando tarefas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    tarefas = session.query(Tarefa).options(joinedload(Tarefa.categoria)).all()
    
    if not tarefas:
        # se não há tarefas cadastradas
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        # retorna a representação da tarefa
        print(tarefas)
        return lista_tarefas(tarefas), 200


@app.get('/tarefa', tags=[tarefa_tag],
         responses={"200": TarefaViewSchema, "404": ErrorSchema})
def get_tarefa(query: TarefaBuscaSchema):   
    
    """Busca uma tarefa pelo ID da tarefa.
    
       Retorna uma representação da tarefa.
    """
    tarefa_id = query.id
        
    logger.debug(f"Coletando dados sobre a tarefa ID #{tarefa_id}")
    
    # cria conexão com a base e faz a busca por id ou descricao
    session = Session()

    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    if tarefa:
        logger.debug(f"Tarefa econtrada: '{tarefa.descricao}'")  
        return exibe_tarefa(tarefa), 200
    else:
        error_msg = "Tarefa não encontrada:/"
        logger.warning(f"Erro ao buscar tarefa '{tarefa_id}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.delete('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaSchema):
    
    """Deleta uma tarefa definitivamente.

       Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_id = unquote(unquote(query.id))
    
    logger.debug(f"Deletando dados da tarefa #{tarefa_id}")
    
    # criando conexão com a base e remove a tarefa
    session = Session()
    count = session.query(Tarefa).filter(Tarefa.id == tarefa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a tarefa #{tarefa_id}")
        return {"mensagem": "Tarefa removida", "id": tarefa_id}
    else:
        error_msg = "Tarefa não encontrada:/"
        logger.warning(f"Erro ao deletar tarefa #'{tarefa_id}', {error_msg}")
        return {"mensagem": error_msg}, 404
    
 
@app.put('/tarefa', tags=[tarefa_tag],
         responses={"200": TarefaUpdateSchema, "404": ErrorSchema})
def update_tarefa(query: TarefaBuscaSchema):
    
    """Atualiza o status de uma tarefa para concluída ou reabre.

       Retorna uma mensagem de confirmação da atualização.
    """
    tarefa_id = unquote(unquote(query.id))
    novo_status = query.concluida
    
    logger.debug(f"Atualizando o status da tarefa #{tarefa_id}")
    
    # criando conexão com a base e atualiza o status da tarefa
    session = Session()
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    
    if tarefa:
        tarefa.concluida = novo_status
        session.commit()
        
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Atualizado o status da tarefa #{tarefa_id}")
        return {"mensagem": "Status da tarefa atualizado", "id": tarefa_id}
    else:
        error_msg = "Tarefa não encontrada:/"
        logger.warning(f"Erro ao atualizar o status da tarefa #'{tarefa_id}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.post('/categoria/', tags=[categoria_tag],
          responses={"200": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_categoria(form: CategoriaSchema):
    """Adiciona uma nova categoria.
     
    """
    
    categoria = Categoria(descricao_categoria=form.descricao_categoria)
    
    logger.debug(f"Adicionando categoria: '{categoria.descricao_categoria}'")
    
    try:
        # cria conexão com a base e adiciona a categoria
        session = Session()
        session.add(categoria)
        session.commit()
        
        logger.debug(f"Adicionado categoria '{categoria.descricao_categoria}'")
        
        return exibe_categoria(categoria), 200

    except IntegrityError as e:
        # erro de integridade do IntegrityError
        error_msg = "Erro de integridade:/"
        logger.warning(f"Erro ao adicionar tarefa '{categoria.descricao_categoria}', {error_msg}")
        
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        print("Erro 422 chegou aqui")
        error_msg = "Não foi possível salvar nova categoria:/"
        logger.warning(f"Erro ao adicionar tarefa '{categoria.descricao_categoria}', {error_msg}")
        
        return {"mensagem": error_msg}, 400
    

@app.get('/categorias', tags=[categoria_tag],
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def get_categorias():
    """Lista todas as categorias cadastradas.

    Retorna uma representação da listagem de categorias.
    """
    logger.debug(f"Coletando categorias ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    categorias = session.query(Categoria).all()
    
    if not categorias:
        # se não há categorias cadastradas
        return {"categorias": []}, 200
    else:
        logger.debug(f"%d categorias encontradas" % len(categorias))
        # retorna a representação da lista de categorias
        print(categorias)
        return lista_categorias(categorias), 200
    
    
@app.delete('/categoria', tags=[categoria_tag],
            responses={"200": CategoriaDelSchema, "404": ErrorSchema})
def del_categoria(query: CategoriaBuscaSchema):
    
    """Deleta uma categoria definitivamente.

       Retorna uma mensagem de confirmação da remoção.
    """
    categoria_id = unquote(unquote(query.id_categoria))
    
    logger.debug(f"Deletando dados da tarefa #{categoria_id}")
    
    # criando conexão com a base e remove a tarefa
    session = Session()
    count = session.query(Categoria).filter(Categoria.id_categoria == categoria_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a categoria #{categoria_id}")
        return {"mensagem": "Categoria removida", "id_categoria": categoria_id}
    else:
        error_msg = "Categoria não encontrada:/"
        logger.warning(f"Erro ao deletar categoria #'{categoria_id}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.get('/categoria/tem_tarefas', tags=[categoria_tag],
        responses={"200": TemTarefasSchema, "404": ErrorSchema})
def tem_tarefas(query: CategoriaBuscaSchema):   
    
    """Verifica se uma categoria tem tarefas associadas.
    
       Retorna um booleano indicando se a categoria tem tarefas associadas.
    """
    id_categoria = query.id_categoria
        
    logger.debug(f"Verificando se a categoria #{id_categoria} tem tarefas associadas")
    
    # cria conexão com a base e faz a busca por fk_categoria
    session = Session()
    count = session.query(func.count(Tarefa.id)).filter(Tarefa.fk_categoria == id_categoria).scalar()

    if count > 0:
        logger.debug(f"Categoria #{id_categoria} tem tarefas associadas")  
        return {"tem_tarefas": {"tem_tarefas": True}}, 200
    else:
        logger.debug(f"Categoria #{id_categoria} não tem tarefas associadas")
        return {"tem_tarefas": {"tem_tarefas": False}}, 200