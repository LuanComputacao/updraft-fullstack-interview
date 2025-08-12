# Updraft Fullstack Interview Project

## Visão Geral

Plataforma multi-tenant para edição e sumarização de documentos, composta por backend Flask (Python) e frontend Vue 3 (Vite), orquestrados via Docker. Persistência em PostgreSQL, proxy reverso com Nginx.

- **Backend:** Flask, arquitetura em camadas (Cosmic Python), comandos Pydantic, serviços transacionais, repositórios SQLAlchemy, DTOs Marshmallow, multi-tenant por hostname.
- **Frontend:** Vue 3 + PrimeVue, editor TipTap, painel lateral para sumário AI, consumo de streaming via Fetch/SSE.
- **Infra:** Docker Compose, Nginx, PostgreSQL.

## Como rodar

Pré-requisitos: Docker, Docker Compose, Node 18+, pnpm

```sh
docker compose up -d
# Aplique as migrations do banco conforme instruções em docs/DEVELOPMENT.md
```

- Backend: http://localhost:3003 (interno: backend:3003)
- Frontend: http://localhost:5180 (interno: frontend:5180)
- Nginx (proxy): http://localdev.localhost:8090

## Estrutura do Projeto

- `backend/components/` — domínio, aplicação, infraestrutura, user_interface
- `frontend/src/` — serviços, componentes, views
- `docs/` — arquitetura, desenvolvimento, UX

## Documentos e Sumário AI

- CRUD de documentos: `/api/documents`
- Sumário AI: `/api/documents/<id>/summary` (persistência), `/stream` (SSE streaming)
- Geração, edição, atualização e deleção de sumários via painel lateral no frontend

## Multi-Tenant

- Tenant derivado do subdomínio (ex: `localdev.localhost`)
- Header `X-Updraft-Tenant` para requests backend

## Variáveis de Ambiente

Veja `backend/.env.sample` e docs/DEVELOPMENT.md para detalhes de configuração de LLM e secrets.

## Testes e QA

- Smoke: criar documento, gerar sumário, salvar, editar, deletar
- Edge: documentos longos, tenant ausente, falha do provider, reconexão SSE

## Documentação

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — visão técnica e decisões
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) — instruções de desenvolvimento
- [docs/UX.md](docs/UX.md) — diretrizes de UX e microinterações

---

Se quiser um README mais detalhado ou com exemplos de uso de API, posso complementar!
