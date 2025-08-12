# Development Guide (James – Dev)

## Run the stack

- Prereqs: Docker, Docker Compose, Node 18+, pnpm
- Start services: `docker compose up -d`
- Apply DB migrations: inside backend container or host, run Alembic as configured
- Backend dev server: `backend/scripts/run-dev.sh` (Flask at :3003)
- Frontend dev server: `pnpm --dir frontend dev` (Vite at :5173, proxied by Nginx in docker)

## Project layout

- Backend: `backend/components/*` following domain/application/infrastructure/user_interface
- Frontend: `frontend/src/*` with services, components, views
- DB migrations: `backend/alembic_scripts/versions/*`

## Documents flow reference

- HTTP POST /api/documents → Pydantic schema → MessageBus → DocumentsService → commit → reopen UoW to read → DTO → JSON.

## Adding Summaries (MVP)

- Backend
  - Create `components/summary` handlers, service, commands
  - Add HTTP endpoints under `/api/documents/<id>/summary` and `/stream`
  - Implement streaming generator with `text/event-stream`
  - Use provider wrapper (OpenAI/Gemini) via an interface
  - Add Alembic migration for summary storage (column or table)
- Frontend
  - Create `src/services/summaryService.ts` for APIs
  - Add component in `src/components/documents/SummaryPanel.vue` using TipTap
  - Stream via Fetch ReadableStream/SSE and update editor content
  - Actions: Generate, Save, Update, Delete

## Testing & QA

- Smoke: create doc, generate summary, save, edit, delete
- Edge cases: very long docs, tenant header missing, provider failure, reconnect stream
- Observability: check logs with X-Request-Id, ensure CORS/compression ok

## Env Vars (.env)

Copy `backend/.env.sample` to `backend/.env` and fill secrets.

- LLM_GOOGLE_API_KEY: Gemini API key (fallback when tenant secret not set)
- LLM_GOOGLE_MODEL: e.g. gemini-2.5-flash (new client) or gemini-1.5-flash (legacy)
- LLM_TEMPERATURE: default 0.3
- LLM_MAX_OUTPUT_TOKENS: default 2048
- LLM_RETRY_ATTEMPTS: default 2
- LLM_RETRY_BACKOFF_S: default 0.5
- LLM_STREAM_TIMEOUT_S: default 120 (seconds)

Tenant header (optional): `X-Updraft-Tenant: <tenant>`

## SSE Contract

- Events: `open` → `chunk` → `done`, or `error`
- `open` data: `{ document_id, request_id }`
- `chunk` data: `{ text, index }`
- `done`: `{}`
- `error` data: `{ message }` (friendly/error-mapped)

## Commit style

- Conventional commits
  - feat(summary): add domain model & migration
  - feat(api): SSE endpoint for summary generation
  - feat(frontend): streaming UI panel
  - chore(dev): scripts and docs
