# Backlog – Document Summarization

Owner: Bob (Scrum Master)
Contributors: Sally (UX), Winston (Architect), James (Dev)

## Sprint Goal

Entregar geração de resumo com streaming e capacidade de salvar/editar/deletar no editor de documentos.

## Epics

- UX: Painel de resumo com TipTap e streaming
- Backend: API de geração e persistência
- Infra/DevEx: chaves de IA, migrações, observabilidade

## User Stories

1. Como usuário, posso gerar um resumo via IA a partir de um documento (streaming)
2. Como usuário, posso salvar o resumo como resumo oficial do documento
3. Como usuário, posso editar o resumo gerado
4. Como usuário, posso deletar o resumo
5. Como usuário, vejo o texto chegando em tempo real enquanto a IA gera o resumo

## Acceptance Criteria (Gherkin)

- Ver DEVELOPMENT.md e UX.md para detalhes; critérios serão vinculados a cada story no board.

## Tasks por Área

### Sally (UX)

- [x] Wireframe do painel lateral "AI Summary" com estados (idle, generating, ready, error)
- [x] Especificar microinterações (spinner, typewriter, cancelar)
- [x] Acessibilidade: ARIA live region, foco, atalhos
- [x] Empty/Loading/Error copy e diretrizes de tom

### Winston (Architecture)

- [x] Decidir contrato de streaming (SSE vs chunked) e padronizar eventos
- [x] Definir modelo de dados (coluna summary em documents vs tabela summaries)
- [x] Planejar migração Alembic e mapeamentos ORM
- [x] Definir interface de provedor de IA
- [x] Estratégia de segredos por tenant (baseline via SecretsManager; docs pendentes)

#### Diretrizes para stores (Pinia)

- [ ] Definir políticas de cache/TTL, invalidação e normalização por domínio
- [ ] Padrões de selectors e separação de responsabilidades (API fina, store orquestra, componente "burro")
- [ ] Convenções de estados/erros (in-flight counter, shape de `error`), logs e telemetria (opcional)

### James (Dev – Backend)

- [x] Criar componente `summary` com domain/application/infrastructure/user_interface
- [x] Endpoints HTTP:
  - [x] POST `/api/documents/<id>/summary/stream` (SSE)
  - [x] GET `/api/documents/<id>/summary`
  - [x] POST `/api/documents/<id>/summary`
  - [x] PUT `/api/documents/<id>/summary`
  - [x] DELETE `/api/documents/<id>/summary`
- [x] Commands/Handlers/Service para salvar/atualizar/deletar
- [x] View/DTO para leitura de resumo
- [x] Integração com provedor IA (mock inicial + real depois)
- [x] Logs estruturados + timeouts; propagar X-Request-Id
- [x] Centralizar prompts do summary em módulo dedicado
- [x] Suporte ao cliente `google-genai` com fallback para `google-generativeai`
- [ ] Testes manuais: long docs, erros do provedor, tenant ausente (iniciado)
- [x] Retries/backoff no provider; timeouts configuráveis por env
- [x] Mapear erros do provedor -> SSE `event:error` e mensagens claras

### James (Dev – Frontend)

- [x] Serviço `summaryService` com fetch streaming (ReadableStream/SSE)
- [x] Componente `SummaryPanel.vue` integrado ao TipTap
- [x] Estados de UI (idle/generating/ready/error) e ações (Generate/Save/Update/Delete)
- [x] Persistência do resumo no documento selecionado
- [x] Tratamento de reconexão e cancelamento do stream

#### Pinia (melhorias)

- [ ] Reorganizar stores em `src/stores/` (mover de `services/stores/`); um módulo por domínio (documents, summary, ui)
- [ ] Documents store normalizado: state `{ byId, allIds, isLoading, error, lastFetchedAt }`; getters `documentsList`, `documentMap`, `documentById(id)`, `count`
- [ ] Actions `fetchCollection({ force, signal })`, `fetchById(id)`, `create`, `update`, `softDelete`, `clear` usando `$patch` e atualizações otimizadas
- [ ] De-duplicar requisições concorrentes e suportar cancelamento com `AbortController`
- [ ] Centralizar erros e toasts; trocar `isLoading` boolean por contador por ação ou flags por ação
- [ ] Router guards: prefetch na entrada da rota de edição/lista; cancelar requisições na saída
- [ ] Summary store: gerenciar streaming (`isGenerating`, `error`, `requestId`, `generatedHtml`); mover SSE do componente para a store; ações `startStream/cancel/save/update/delete` com retry/backoff alinhado
- [ ] Resetar stores ao trocar tenant (`store.$reset`) e invalidar cache (TTL)
- [ ] Plugins Pinia (logger, persistedstate) e tipagem (JSDoc/TypeScript) para melhor DX
- [ ] Testes básicos de stores com mocks do API (fetch/create/update/delete)
- [ ] Documentar padrões de stores em `DEVELOPMENT.md` (estrutura, normalização, selectors, erros)

### Infra/DevEx

- [x] Variáveis de ambiente para chaves (OpenAI/Gemini) e limites
- [ ] Docker/compose: propagar segredos com segurança
- [x] Alembic: criar migração e aplicar
- [ ] Observabilidade: logs no backend, mensagens claras no frontend
- [x] Script de teste do cliente `google-genai` (ad-hoc)
- [x] Documentar envs no README/DEVELOPMENT e adicionar `.env.sample`
- [x] Documentar SSE/Nginx e cabeçalho `X-Updraft-Tenant`

## Definition of Done

- Endpoints funcionam e documentados no README/DEVELOPMENT
- Streaming visível na UI e cancelável
- Resumo salvo/editável/deletável
- Sem erros no console; CORS/Compress configurados
- Migrações aplicadas; build Docker ok

## Riscos

- Limites de tokens e custos da IA
- Reconexões SSE sob proxies
- Latência para documentos grandes
