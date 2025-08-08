# UpDraft App Architecture (Winston – Architect)

## Overview

- Multi-tenant Flask backend + Vue 3 frontend.
- Layered architecture (Cosmic Python): domain → application → infrastructure → user_interface.
- PostgreSQL single physical DB with tenant scoping; Nginx reverse proxy; Docker for orchestration.

## Backend

- Message Bus per request: `components/shared/application/message_bus.py`. Fresh bus via factory in each HTTP handler. Results in `bus.results`.
- Unit of Work: `SqlAlchemyUnitOfWork` wires repositories. Pattern: `with uow:` then `commit()`.
- Repositories: thin CRUD wrappers, `seen` for future events. ORM via imperative mapping; `start_mappers()` on app bootstrap.
- Commands: Pydantic models under each domain (e.g., documents: `components/documents/domain/commands.py`).
- Services: transaction scripts (e.g., `DocumentsService`) operating via UoW; handlers bound in `application/handler_maps.py`.
- Views/DTOs: Query side reads via SQLAlchemy and serializes with Marshmallow DTOs.
- HTTP: Blueprints in `user_interface/http`, parse/validate with `parse_with_for_http`.
- Tenant: set by middleware (`set_tenant`), accessed with context var.

## Implemented Slice: Documents

- Endpoints `/api/documents`: create, update, soft-delete, get, list.
- Flow: HTTP → parse → Command → Bus → Service (UoW commit) → read-back via view → DTO.

## Summarization Feature Plan

- New component `components/summary` mirroring structure (domain/application/infrastructure/user_interface).
- Endpoints:
  - POST `/api/documents/<id>/summary/stream` (SSE or chunked JSON) to stream AI tokens.
  - POST `/api/documents/<id>/summary` to persist final summary.
  - PUT `/api/documents/<id>/summary` to update; DELETE to soft-delete; GET to fetch.
- Storage: either `documents.summary` column (MVP) or a `summaries` table (history, edits). Alembic migration required.
- AI Integration: wrap provider behind interface (OpenAI/Gemini) with tenant-aware secret manager. Use server-side streaming generator.
- Frontend: Vue service for streaming (Fetch ReadableStream), side panel with TipTap editor, Save/Update/Delete actions.
- Observability: request-id propagation, structured logs, timeout and retry policy on AI provider.

## Decisions & Trade-offs

- Start with single summary per document (column) for speed; refactor to table if time permits.
- SSE vs chunked JSON: choose text/event-stream for simplicity and browser support.
- Keep commands for mutations; reads via views.

## Open Questions

- Should archived documents be excluded from summarization endpoints?
- Provider choice and token limits per tenant.
