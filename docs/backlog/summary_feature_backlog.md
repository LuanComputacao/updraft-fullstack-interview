# Backlog – Document Summarization

Owner: Bob (Scrum Master)
Contributors: Sally (UX), Winston (Architect), James (Dev)

## Sprint Goal

Deliver summary generation with streaming and ability to save/edit/delete inside the document editor.

## Epics

- UX: Summary panel with TipTap and streaming
- Backend: Generation & persistence API
- Infra/DevEx: AI keys, migrations, observability

## User Stories

1. As a user, I can generate a summary via AI from a document (streaming)
2. As a user, I can save the summary as the official document summary
3. As a user, I can edit the generated summary
4. As a user, I can delete the summary
5. As a user, I see text arriving in real time while AI generates the summary

## Acceptance Criteria (Gherkin)

- See DEVELOPMENT.md and UX.md for details; criteria will be linked to each story on the board.

## Tasks by Area

### Sally (UX)

- [x] Wireframe for side panel "AI Summary" with states (idle, generating, ready, error)
- [x] Specify micro-interactions (spinner, typewriter, cancel)
- [x] Accessibility: ARIA live region, focus, shortcuts
- [x] Empty/Loading/Error copy and tone guidelines

### Winston (Architecture)

- [x] Decide streaming contract (SSE vs chunked) and standardize events
- [x] Define data model (summary column in documents vs summaries table)
- [x] Plan Alembic migration and ORM mappings
- [x] Define AI provider interface
- [x] Strategy for secrets per tenant (baseline via SecretsManager; docs pending)

#### Guidelines for stores (Pinia)

- [ ] Define cache/TTL, invalidation and normalization per domain
- [ ] Patterns for selectors and separation of responsibilities (thin API, store orchestrates, dumb component)
- [ ] Conventions for states/errors (in-flight counter, shape of `error`), logs & telemetry (optional)

### James (Dev – Backend)

- [x] Create `summary` component with domain/application/infrastructure/user_interface
- [x] HTTP endpoints:
  - [x] POST `/api/documents/<id>/summary/stream` (SSE)
  - [x] GET `/api/documents/<id>/summary`
  - [x] POST `/api/documents/<id>/summary`
  - [x] PUT `/api/documents/<id>/summary`
  - [x] DELETE `/api/documents/<id>/summary`
- [x] Commands/Handlers/Service to save/update/delete
- [x] View/DTO for summary read
- [x] Integration with AI provider (initial mock + real later)
- [x] Structured logs + timeouts; propagate X-Request-Id
- [x] Centralize summary prompts in dedicated module
- [x] Support `google-genai` client with fallback to `google-generativeai`
- [ ] Manual tests: long docs, provider errors, missing tenant (started)
- [x] Retries/backoff in provider; timeouts configurable via env
- [x] Map provider errors -> SSE `event:error` with clear messages

### James (Dev – Frontend)

- [x] `summaryService` with streaming fetch (ReadableStream/SSE)
- [x] `SummaryPanel.vue` component integrated with TipTap
- [x] UI states (idle/generating/ready/error) and actions (Generate/Save/Update/Delete)
- [x] Summary persistence in selected document
- [x] Handling stream reconnection and cancellation

#### Pinia (improvements)

- [ ] Reorganize stores into `src/stores/` (move from `services/stores/`); one module per domain (documents, summary, ui)
- [ ] Documents store normalized: state `{ byId, allIds, isLoading, error, lastFetchedAt }`; getters `documentsList`, `documentMap`, `documentById(id)`, `count`
- [ ] Actions `fetchCollection({ force, signal })`, `fetchById(id)`, `create`, `update`, `softDelete`, `clear` using `$patch` and optimized updates
- [ ] De-duplicate concurrent requests and support cancellation with `AbortController`
- [ ] Centralize errors and toasts; replace boolean `isLoading` with counter per action or flags per action
- [ ] Router guards: prefetch on entering edit/list route; cancel requests on leave
- [ ] Summary store: manage streaming (`isGenerating`, `error`, `requestId`, `generatedHtml`); move SSE from component to store; actions `startStream/cancel/save/update/delete` with retry/backoff alignment
- [ ] Reset stores when tenant changes (`store.$reset`) and invalidate cache (TTL)
- [ ] Pinia plugins (logger, persistedstate) and typing (JSDoc/TypeScript) for better DX
- [ ] Basic store tests with mocked API (fetch/create/update/delete)
- [ ] Document store patterns in `DEVELOPMENT.md` (structure, normalization, selectors, errors)

### Infra/DevEx

- [x] Environment variables for keys (OpenAI/Gemini) and limits
- [ ] Docker/compose: propagate secrets securely
- [x] Alembic: create migration and apply
- [ ] Observability: backend logs, clear frontend messages
- [x] Test script for `google-genai` client (ad-hoc)
- [x] Document envs in README/DEVELOPMENT and add `.env.sample`
- [x] Document SSE/Nginx and `X-Updraft-Tenant` header

## Definition of Done

- Endpoints working and documented in README/DEVELOPMENT
- Streaming visible in UI and cancelable
- Summary saved/editable/deletable
- No console errors; CORS/Compression configured
- Migrations applied; Docker build OK

## Risks

- AI token limits and costs
- SSE reconnections under proxies
- Latency for large documents
