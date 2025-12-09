# 🚀 Projeto MultiContainer — CI/CD com GitHub Actions, Docker Hub e VPS

![CI/CD Pipeline](https://github.com/vitoriarx/projetoMultiContainer/actions/workflows/cicd.yml/badge.svg)

Este repositório contém um pipeline completo de **Integração Contínua (CI)** e **Entrega Contínua (CD)** utilizando:

- **GitHub Actions**
- **Docker Hub**
- **Docker Buildx**
- **Docker Compose (produção & desenvolvimento)**
- **Deploy automático na VPS via SSH**

O objetivo é garantir que qualquer push para a branch `main` resulte em:

1. Execução automática de testes 🔍  
2. Build da imagem Docker da API 🐳  
3. Publicação da imagem no Docker Hub 📦  
4. Atualização automática dos containers na VPS 🚀  

---

# 📁 Estrutura do Projeto

```bash 
projetoMultiContainer/
│
├── app/ # Código da API Python
│ ├── main.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── docker-compose.yml # Ambiente local
├── docker-compose.prod.yml # Ambiente de produção (VPS)
│
└── .github/workflows/cicd.yml # Pipeline completo de CI/CD
```


---

# ⚙️ Pipeline CI/CD — Visão Geral

O arquivo `cicd.yml` executa 2 jobs principais:

---

## 🔵 1. BUILD & TEST

**O que ele faz?**

- Faz checkout do repositório
- Instala dependências Python
- Executa testes automáticos com PyTest
- Faz login no Docker Hub
- Faz build da imagem Docker da API
- Publica no Docker Hub com duas tags:
  - SHA da versão: `vitoriarx/projetodevops-api:<commit>`
  - Latest: `vitoriarx/projetodevops-api:latest`

---

## 🟢 2. DEPLOY AUTOMÁTICO (CD)

Depois da etapa anterior passar, o GitHub Actions:

- Acessa a VPS via SSH  
- Entra na pasta do projeto  
- Atualiza a imagem do Docker Hub  
- Recria os containers com `docker-compose.prod.yml`  
- Sobe o ambiente em produção  

Tudo isso sem você precisar fazer nada manualmente. 🎯

---

# 🔧 Variáveis de Ambiente Necessárias (GitHub Secrets)

| Nome | Descrição |
|------|-----------|
| **DOCKERHUB_USERNAME** | Seu usuário do Docker Hub |
| **DOCKERHUB_TOKEN** | Token de acesso (não senha) |
| **SSH_HOST** | IP da VPS |
| **SSH_USER** | Usuário (ex: root) |
| **SSH_KEY** | Chave privada da VPS |
| **PROJECT_PATH** | Caminho onde está o projeto na VPS |
| **DB_PASSWORD** | Senha usada no docker-compose.prod.yml |

---

# 🐳 Rodando o projeto localmente

### 🔹 Subir containers no ambiente local:

```bash
docker compose up --build
```
🔹 Parar containers:
```bash
docker compose down
```

🛠 Arquivo docker-compose.prod.yml (produção)

A versão de produção faz pull da imagem direto do Docker Hub: 

```bash
services:
  api:
    image: vitoriarx/projetodevops-api:latest
    restart: always
    environment:
      - DB_PASSWORD=${DB_PASSWORD}
    ports:
      - "8000:8000"
```

🚀 Deploy automático na VPS

Qualquer push para main dispara o pipeline.

Ao chegar no job deploy, ele executa na VPS: 

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --remove-orphans
```
🧪 Testes

Para rodar os testes localmente:
```bash
pytest
```

📌 Badge do pipeline: 

![Build Status](https://img.shields.io/github/actions/workflow/status/vitoriarx/projetoMultiContainer/cicd.yml?branch=main)
