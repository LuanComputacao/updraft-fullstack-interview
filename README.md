# Updraft Fullstack Interview Project

## Overview

Multi-tenant platform for document editing and AI summarization, composed of a Flask (Python) backend and a Vue 3 (Vite) frontend, orchestrated via Docker. Persistence in PostgreSQL, reverse proxy with Nginx.

- **Backend:** Flask, layered (Cosmic Python) architecture, Pydantic command objects, transactional services, SQLAlchemy repositories, Marshmallow DTOs, multi-tenant by hostname.
- **Frontend:** Vue 3 + PrimeVue, TipTap editor, side panel for AI summary, streaming consumption via Fetch/SSE.
- **Infrastructure:** Docker Compose, Nginx, PostgreSQL.

## How to Run

Prerequisites: Docker, Docker Compose, Node 18+, pnpm

```sh
docker compose up -d
# Apply database migrations as described in docs/DEVELOPMENT.md
```

- Backend: http://localhost:3003 (internal: backend:3003)
- Frontend: http://localhost:5180 (internal: frontend:5180)
- Nginx (proxy): http://localdev.localhost:8090

## Project Structure

- `backend/components/` — domain, application, infrastructure, user_interface
- `frontend/src/` — services, components, views
- `docs/` — architecture, development, UX

## Documents and AI Summary

- Documents CRUD: `/api/documents`
- AI Summary: `/api/documents/<id>/summary` (persistence), `/stream` (SSE streaming)
- Generate, edit, update and delete summaries via the side panel in the frontend

## Multi-Tenant

- Tenant derived from subdomain (e.g. `localdev.localhost`)
- Header `X-Updraft-Tenant` required in backend requests

## Environment Variables

See `backend/.env.sample` and `docs/DEVELOPMENT.md` for LLM and secrets configuration details.

## Tests and QA

- Smoke: create document, generate summary, save, edit, delete
- Edge: long documents, missing tenant, provider failure, SSE reconnection

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — technical view and decisions
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) — development instructions
- [docs/UX.md](docs/UX.md) — UX guidelines and micro-interactions

---

If you want a more detailed README or API usage examples, just ask!
