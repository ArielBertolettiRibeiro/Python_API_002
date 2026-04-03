# Sistema de Gestão de Estoque e Movimentações

API REST para gerenciamento de estoque e controle de movimentações de produtos, desenvolvida em Python.

---

## Sobre o Projeto

Sistema backend que permite o controle completo do ciclo de vida de produtos em estoque, incluindo entradas, saídas, transferências e rastreabilidade das movimentações.

---

## Funcionalidades

- Cadastro e gerenciamento de produtos
- Controle de categorias e fornecedores
- Registro de entradas e saídas de estoque
- Histórico completo de movimentações
- Alertas de estoque mínimo
- Relatórios de inventário

---

## Tecnologias

- **Python 3.11+**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **PostgreSQL** — banco de dados
- **Pydantic** — validação de dados
- **Alembic** — migrações de banco
- **JWT** — autenticação

---

## Estrutura do Projeto

```
Python_API_002/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── services/
├── tests/
├── alembic/
├── .env.example
├── requirements.txt
└── README.md
```

---

## Como Executar

### Pré-requisitos

- Python 3.11+
- PostgreSQL

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Python_API_002

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações
```

### Configuração do `.env`

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/estoque_db
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Executando a API

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em: `http://localhost:8000/docs`

---

## Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/login` | Autenticação |
| GET | `/produtos` | Listar produtos |
| POST | `/produtos` | Cadastrar produto |
| PUT | `/produtos/{id}` | Atualizar produto |
| DELETE | `/produtos/{id}` | Remover produto |
| GET | `/estoque` | Consultar estoque |
| POST | `/movimentacoes/entrada` | Registrar entrada |
| POST | `/movimentacoes/saida` | Registrar saída |
| GET | `/movimentacoes` | Histórico de movimentações |
| GET | `/relatorios/inventario` | Relatório de inventário |

---

## Testes

```bash
pytest
```

---

## Autor

**ArielBertolettiRibeiro**
