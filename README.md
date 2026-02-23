🚀 lICIPRO SaaS – Plataforma de Inteligência em Licitações Públicas

Sistema SaaS multi-tenant desenvolvido com FastAPI + SQLAlchemy + JWT Authentication, voltado para empresas que atuam em licitações públicas.

A plataforma permite gerenciamento de usuários por empresa, autenticação segura com OAuth2, e está estruturada para futura integração com bases públicas como Compras.gov.br e Portal Nacional de Contratações Públicas.

🧠 Arquitetura

🔐 Autenticação JWT com OAuth2

🏢 Multi-tenant (Company → Users)

👤 Controle de permissões (admin / user)

📦 Estrutura pronta para planos (free, pro, enterprise)

🛠️ Backend escalável preparado para consumo de dados públicos

🛠️ Stack Utilizada

FastAPI

SQLAlchemy

PostgreSQL (ou SQLite em dev)

Passlib (bcrypt)

Python-JOSE (JWT)

Swagger UI

📌 Funcionalidades Implementadas

Cadastro de empresa + usuário administrador

Login seguro com geração de token

Rotas protegidas

Estrutura multi-empresa isolada

Base para expansão de BI e geração automática de documentos

📈 Roadmap

Integração com dados públicos de licitações

Dashboard analítico

Ranking de marcas vencedoras

Geração automática de documentos de habilitação

Alertas inteligentes por segmento

## Como rodar

uvicorn app.main:app --reload
