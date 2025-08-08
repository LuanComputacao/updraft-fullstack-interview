# Tech Spec – Document Summarization (Guia para James – Dev)

Objetivo

Implementar geração de resumo com streaming e CRUD de persistência seguindo a arquitetura existente (Cosmic Python), mantendo isolamento por tenant e boas práticas de observabilidade.

Arquitetura e Contratos

- Protocolo de streaming: SSE (text/event-stream) via Fetch ReadableStream. Enviar cabeçalhos: Cache-Control: no-cache, Connection: keep-alive, X-Accel-Buffering: no.
- Persistência: coluna documents.summary_html (TEXT, nullable). MVP sem histórico.
- Componente novo: backend/components/summary com camadas domain/application/infrastructure/user_interface.
- Provider IA: interface SummaryProvider (mock inicial; depois OpenAI/Gemini via SecretManager).

Banco de Dados

- Alembic revision: adicionar coluna summary_html à tabela documents.
  - Nome: 12748679d72e_add_summary_field_to_documents (seguir padrão existente)
  - ORM: incluir Column("summary_html", Text, nullable=True) em components/documents/infrastructure/orm.py

Domain (summary)

- commands.py
  - GenerateSummary(document_id: UUID, options: dict | None = None) – streaming (não persiste)
  - SaveSummary(document_id: UUID, content_html: str)
  - UpdateSummary(document_id: UUID, content_html: str)
  - DeleteSummary(document_id: UUID)

Application (summary)

- summary_service.py
  - generate_stream(cmd):
    - abrir uow, carregar Document; validar archived_at is None
    - chamar provider.stream_summary(document.content_html, options)
    - yield chunks str (ou dict {text})
  - save/update/delete(cmd):
    - with uow: setar document.summary_html, commit
- handler_maps.py
  - Mapear comandos → métodos do SummaryService

Infrastructure (summary)

- providers.py
  - interface SummaryProvider
  - MockProvider: rendeza chunks simulados
  - OpenAI/Gemini: usar SecretManagerInterface.get_tenant_secrets()["ai"], timeout/retry

User Interface HTTP (summary)

- user_interface/http/summary_api.py
  - POST /api/documents/{uuid:document_id}/summary/stream
    - Body opcional: { style?, length?, prompt? }
    - Resposta SSE com eventos:
      - event: open → data: {"document_id": "..."}
      - event: chunk → data: {"text": "...", "index": n}
      - event: done → data: {"usage": {...}}
      - event: error → data: {"message": "..."}
  - GET /api/documents/{uuid}/summary → { document_id, summary_html }
  - POST /api/documents/{uuid}/summary → persiste summary_html
  - PUT /api/documents/{uuid}/summary → atualiza summary_html
  - DELETE /api/documents/{uuid}/summary → summary_html = null
- schemas.py
  - Save/Update payload: { content_html: string }
- bus.py
  - factory para criar MessageBus com Summary handlers (novo por request)

Integrações e Bootstrap

- app.py
  - registrar summary_blueprint em register_blueprints
- components/shared/user_interface/http_api/http_error_mappers.py
  - mapear novos erros: DocumentNotFound, CannotUpdateArchivedDocument, ProviderError

Observabilidade & Tenant

- Propagar X-Request-Id (já existe); logar início/fim de stream e erros do provider
- Garantir tenant via middleware; provider lê segredos por tenant

Frontend (referência rápida)

- services/summaryService.ts
  - streamSummary(documentId, options, onEvent)
  - get/save/update/delete
- components/documents/SummaryPanel.vue
  - Estados: idle/generating/ready/error; TipTap para summary_html
  - A11y: ARIA live polite; foco e atalhos conforme docs/ux

Sequência de Commits (sugerida)

1. feat(db): alembic add summary_html em documents + mapper
2. feat(summary): scaffolding (domain/application/.../bus, handler_maps)
3. feat(api): endpoints CRUD de resumo + DTOs/views
4. feat(api): SSE /summary/stream com MockProvider
5. feat(frontend): summaryService + SummaryPanel.vue (stream + CRUD)
6. feat(provider): integração real via SecretManager
7. chore(obs): logs, timeouts, headers SSE e ajustes Nginx

Critérios de Teste Manual

- Gerar resumo em doc existente: ver chunks chegando e done
- Cancelar geração: conexão fecha, texto parcial preservado
- Salvar/editar/deletar: GET reflete mudanças; reabrir página mantém estado
- Tenant ausente: 403; erros do provider: evento error + mensagem na UI
