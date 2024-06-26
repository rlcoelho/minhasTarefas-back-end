# Back-end do sistema Minhas Tarefas

A proposta do **Minhas Tarefas** é ser um sistema simples para o registro de compromissos. A intenção é oferecer ao usuário uma experiência de uso fácil, como se ele estivesse diante de um bloco de papel e uma caneta.

Diferente de outras ferramentas mais robustas e com diversos controles e configurações que muitas vezes não são utilizados ou causam confusão em seu uso, o **Minhas Tarefas** organiza as tarefas previstas por categorias e o usuário tem total controle sobre a criação das tarefas e das categorias.

Back-end desenvolvido na linguagem Python com o microframework web Flask, framework ORM SQLAlchemy e banco de dados embutido SQLite3, além de outras bibliotecas do Python.

O front-end que integra o sistema **Minhas Tarefas** foi desenvolvido no formato de Single Page Application (SPA) utilizando HTML, CSS e JavaScript. Possui design responsivo e alguns recursos de acessibilidade, como tags semânticas e textos alternativos nos ícones de interação.

---
## Repositório do front-end

Este back-end necessita do front-end que está disponível no repositório: https://github.com/rlcoelho/minhasTarefas-front-end

---
## Como executar 

Este projeto requer que você tenha instalado em seu sistema o Python 3.11 ou superior e o banco de dados SQLite3.

Será necessário ter instaladas todas as libs Python listadas no arquivo `requirements.txt`.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
## Melhorias previstas

1) Criação de filtro para exibir na tela "Todas as tarefas":
    a) todas as tarefas.
    b) somente as tarefas que não estão concluídas.
    c) somente as tarefas que estão concluídas.
    d) tarefas por data prevista.
    e) tarefas da semana atual.

2) Criação de nova tela inicial com as tarefas da semana atual e que permita paginação entre a semana anterior e a próxima semana.

3) Paginação das listas de tarefas e de categorias com o usuário escolhendo a quantidade de registros que deseja exibir.

4) Opção para alteração de todos os dados de uma tarefa cadastrada.

5) Permitir a vinculação entre tarefas criando uma opção de relacionar uma tarefa a outra.

6) Relatórios diversos.

7) Serviços de notificações com alertas próximos a data prevista.

