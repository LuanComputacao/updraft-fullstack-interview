# Tech Spec – Document Summarization (Guide for James – Dev)

Objective

Implement summary generation with streaming and persistence CRUD following the existing architecture (Cosmic Python), maintaining tenant isolation and observability best practices.

Architecture & Contracts

- Streaming protocol: SSE (text/event-stream) via Fetch ReadableStream. Send headers: Cache-Control: no-cache, Connection: keep-alive, X-Accel-Buffering: no.
- Persistence: column documents.summary_html (TEXT, nullable). MVP without history.
- New component: backend/components/summary with domain/application/infrastructure/user_interface layers.
- AI Provider: SummaryProvider interface (initial mock; later OpenAI/Gemini via SecretManager).

Database

- Alembic revision: add column summary_html to documents table.
  - Name: 12748679d72e_add_summary_field_to_documents (follow existing pattern)
  - ORM: include Column("summary_html", Text, nullable=True) in components/documents/infrastructure/orm.py

Domain (summary)

- commands.py
  - GenerateSummary(document_id: UUID, options: dict | None = None) – streaming (does not persist)
  - SaveSummary(document_id: UUID, content_html: str)
  - UpdateSummary(document_id: UUID, content_html: str)
  - DeleteSummary(document_id: UUID)

Application (summary)

- summary_service.py
  - generate_stream(cmd):
    - open uow, load Document; validate archived_at is None
    - call provider.stream_summary(document.content_html, options)
    - yield chunks str (or dict {text})
  - save/update/delete(cmd):
    - with uow: set document.summary_html, commit
- handler_maps.py
  - Map commands → SummaryService methods

Infrastructure (summary)

- providers.py
  - SummaryProvider interface
  - MockProvider: renders simulated chunks
  - OpenAI/Gemini: use SecretManagerInterface.get_tenant_secrets()["ai"], timeout/retry

User Interface HTTP (summary)

- user_interface/http/summary_api.py
  - POST /api/documents/{uuid:document_id}/summary/stream
    - Optional body: { style?, length?, prompt? }
    - SSE response with events:
      - event: open → data: {"document_id": "..."}
      - event: chunk → data: {"text": "...", "index": n}
      - event: done → data: {"usage": {...}}
      - event: error → data: {"message": "..."}
  - GET /api/documents/{uuid}/summary → { document_id, summary_html }
  - POST /api/documents/{uuid}/summary → persist summary_html
  - PUT /api/documents/{uuid}/summary → update summary_html
  - DELETE /api/documents/{uuid}/summary → summary_html = null
- schemas.py
  - Save/Update payload: { content_html: string }
- bus.py
  - factory to create MessageBus with Summary handlers (new per request)

Integrations & Bootstrap

- app.py
  - register summary_blueprint in register_blueprints
- components/shared/user_interface/http_api/http_error_mappers.py
  - map new errors: DocumentNotFound, CannotUpdateArchivedDocument, ProviderError

Observability & Tenant

- Propagate X-Request-Id (already exists); log start/end of stream and provider errors
- Guarantee tenant via middleware; provider reads secrets per tenant

Frontend (quick reference)

- services/summaryService.ts
  - streamSummary(documentId, options, onEvent)
  - get/save/update/delete
- components/documents/SummaryPanel.vue
  - States: idle/generating/ready/error; TipTap for summary_html
  - A11y: ARIA live polite; focus & shortcuts per docs/ux

Suggested Commit Sequence

1. feat(db): alembic add summary_html in documents + mapper
2. feat(summary): scaffolding (domain/application/.../bus, handler_maps)
3. feat(api): summary CRUD endpoints + DTOs/views
4. feat(api): SSE /summary/stream with MockProvider
5. feat(frontend): summaryService + SummaryPanel.vue (stream + CRUD)
6. feat(provider): real integration via SecretManager
7. chore(obs): logs, timeouts, SSE headers and Nginx adjustments

Manual Test Criteria

- Generate summary on existing doc: see chunks arriving and done
- Cancel generation: connection closes, partial text preserved
- Save/edit/delete: GET reflects changes; reopen page keeps state
- Missing tenant: 403; provider errors: event error + message in UI
