# Docker CRUD Flask + PostgreSQL

Um projeto de exemplo de **API CRUD em Python com Flask** utilizando **PostgreSQL** em ambiente **multi-container com Docker Compose**.  

O projeto inclui:

- CRUD de **usuários** e **produtos**.
- Persistência de dados via **volumes**.
- Configuração de **variáveis de ambiente**.
- Usuário de aplicação dedicado (não root) para segurança.
- Estrutura modular e documentação completa.

---

## 🔧 Pré-requisitos

Antes de começar, você precisa ter instalado:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

---

## 📁 Estrutura do Projeto
```bash
docker-crud/
│
├── app/
│ ├── main.py # Código da API Flask
│ ├── requirements.txt # Dependências Python
│ └── Dockerfile # Dockerfile da aplicação
│
├── docker-compose.yml # Configuração dos containers
├── .env # Variáveis de ambiente
├── init.sql # Script de inicialização do banco
└── README.md
```

---

## 🛠 Configuração do Banco de Dados

Arquivo `.env` com variáveis sensíveis:

```env
POSTGRES_DB=mydb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=app123
DB_HOST=db
DB_NAME=mydb
DB_USER=appuser
DB_PASS=app123
Script init.sql para criar tabelas:
```

```bash
-- Usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

```bash
-- Produtos
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    stock INT
);
```

🐳 Docker Compose
Exemplo do docker-compose.yml:

```bash
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: postgres_db
    env_file: .env
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - mynetwork

  flask_api:
    build:
      context: ./app
    container_name: flask_api
    ports:
      - "5000:5000"
    env_file: .env
    depends_on:
      - db
    networks:
      - mynetwork

volumes:
  db_data:

networks:
  mynetwork:
```

🚀 Como Executar o Projeto
Clonar o repositório:

```bash
git clone https://github.com/vitoriarx/ambienteMultiContainer
cd docker-crud
```

Subir os containers com Docker Compose:
```bash
docker-compose up --build
A API estará disponível em: http://localhost:5000
```
O PostgreSQL estará rodando no container postgres_db.

🔹 Testar os Endpoints (via curl)
Usuários
Listar usuários:
```bash
curl http://localhost:5000/users
```

Adicionar usuário:
```bash
curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d "{\"name\":\"Vitória Melo\",\"email\":\"vitoria@email.com\"}"
```

Atualizar usuário:
```bash
curl -X PUT http://localhost:5000/users/1 \
-H "Content-Type: application/json" \
-d "{\"name\":\"Vitória R. Melo\",\"email\":\"vitoria@email.com\"}"
```

Deletar usuário:

```bash
curl -X DELETE http://localhost:5000/users/1
```

Produtos
Listar produtos:

```bash
curl http://localhost:5000/products

```

```bash
Adicionar produto:

curl -X POST http://localhost:5000/products \
-H "Content-Type: application/json" \
-d "{\"name\":\"Camiseta\",\"price\":49.90,\"stock\":10}"
```

Atualizar produto:


```bash
curl -X PUT http://localhost:5000/products/1 \
-H "Content-Type: application/json" \
-d "{\"name\":\"Camiseta Premium\",\"price\":59.90,\"stock\":15}"

```

Deletar produto:

```bash
curl -X DELETE http://localhost:5000/products/1

```

🔒 Segurança
Usuário de aplicação (appuser) configurado no .env.

Banco não roda operações críticas com root.

Variáveis sensíveis não estão hardcoded no código.

💾 Persistência de Dados
Dados do banco persistem no volume Docker db_data.

Mesmo que os containers sejam removidos, os dados permanecem.

📌 Subir o Projeto para o GitHub
Inicializar repositório local:

```bash
git init
git add .
git commit -m "Projeto Docker CRUD Flask + PostgreSQL"
Criar repositório no GitHub e copiar a URL (https://github.com/vitoriarx/ambienteMultiContainer)

```
Adicionar remoto e enviar:

```bash
git remote add origin https://github.com/vitoriarx/ambienteMultiContainer
git branch -M main
git push -u origin main
```

# 🐳 Arquitetura do Projeto - Flask + PostgreSQL (Docker)

                 ┌──────────────────────────────┐
                 │        🧠 Docker Desktop     │
                 │   (Ambiente de Containers)   │
                 └──────────────────────────────┘
                                │
                                ▼
       ┌────────────────────────────────────────────────┐
       │               🌐 Docker Network               │
       │             (mynetwork interna)                │
       │                                                │
       │   ┌────────────────────┐       ┌──────────────────────┐
       │   │  ⚙️ Container       │       │ 🧩 Container       │
       │   │  flask_api          │◀────▶│ postgres_db         │
       │   │--------------------│       │----------------------│
       │   │  - Flask (Python)  │       │  - PostgreSQL        │
       │   │  - SQLAlchemy      │       │  - Porta 5432        │
       │   │  - Porta 5000      │       │  - Usuário: user     │
       │   │                    │       │  - Banco: product_db │
       │   └────────────────────┘       └──────────────────────┘
       │             ▲                             │
       │             │                             ▼
       │             │                    ┌────────────────────── ┐
       │             │                    │ 💾 Volume Persistente│
       │             │                    │ (db_data)             │
       │             │                    │ Armazena dados mesmo  │
       │             │                    │ após reiniciar        │
       │             │                    └────────────────────── ┘
       └────────────────────────────────────────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ 💻 Usuário / Navegador       │
                 │ http://localhost:5000        │
                 └──────────────────────────────┘
