# CRUD Genérico — Flask + SQLite + JS Puro

Sistema **CRUD (Create, Read, Update, Delete)** genérico, construído com
**Python (Flask)** no backend, **SQLite** como banco de dados (SQL puro,
sem ORM) e um frontend simples em **HTML, CSS e JavaScript puro**.

O projeto gerencia uma entidade genérica chamada **Item**, mas foi
estruturado para ser facilmente adaptado a qualquer outro domínio
(produtos, clientes, tarefas, contatos, etc.) — basta ajustar a tabela,
os campos e o formulário.

## Funcionalidades

- ✅ Criar, listar, editar e excluir itens
- ✅ Busca por nome (`?q=`)
- ✅ Validação de dados (campos obrigatórios, tipos)
- ✅ API REST documentada com códigos HTTP corretos
- ✅ Frontend simples consumindo a API via `fetch`
- ✅ Tratamento de erros (404, dados inválidos, etc.)

## Tecnologias

| Camada    | Tecnologia               |
|-----------|---------------------------|
| Backend   | Python 3 + Flask           |
| Banco     | SQLite (via `sqlite3`)     |
| Frontend  | HTML5, CSS3, JavaScript    |

## Estrutura do projeto

```
crud-portfolio/
├── app.py                 # Aplicação Flask + rotas da API
├── requirements.txt       # Dependências do projeto
├── templates/
│   └── index.html         # Página principal (frontend)
├── static/
│   ├── style.css           # Estilos
│   └── script.js            # Lógica de consumo da API
└── database.db             # Criado automaticamente (SQLite)
```

## Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/crud-portfolio.git
cd crud-portfolio

# 2. Crie um ambiente virtual (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
python app.py
```

Acesse **http://127.0.0.1:5000** no navegador.

## Endpoints da API

| Método | Rota                | Descrição                          |
|--------|----------------------|--------------------------------------|
| GET    | `/api/itens`          | Lista todos os itens (`?q=` busca)   |
| GET    | `/api/itens/<id>`     | Retorna um item específico           |
| POST   | `/api/itens`          | Cria um novo item                    |
| PUT    | `/api/itens/<id>`     | Atualiza um item existente           |
| DELETE | `/api/itens/<id>`     | Remove um item                       |

### Exemplo — criar item

```bash
curl -X POST http://127.0.0.1:5000/api/itens \
  -H "Content-Type: application/json" \
  -d '{"nome": "Caneta Azul", "descricao": "Esferográfica", "quantidade": 10}'
```

## Adaptando para outro domínio

Para reutilizar este CRUD com outra entidade (ex: "Produtos" ou
"Clientes"):

1. Ajuste a criação da tabela em `criar_banco()` no `app.py`.
2. Atualize os campos usados nas rotas (`nome`, `descricao`, `quantidade`).
3. Ajuste o formulário em `templates/index.html` e o JS em `static/script.js`.

## Autor

**Jadinei G. Xavier**
Desenvolvido como projeto de portfólio.

## Licença 

Este projeto está sob a licença MIT — sinta-se livre para usar e adaptar. 
Vlwww.
