# SSE and Nginx Configuration

This app streams AI summary tokens via Server-Sent Events (SSE).

## Backend

- Endpoint: POST `/api/documents/<id>/summary/stream`
- Headers set by Flask response:
  - `Content-Type: text/event-stream`
  - `Cache-Control: no-cache`
  - `Connection: keep-alive`
  - `X-Accel-Buffering: no`
- Events:
  - `open` → data `{ document_id, request_id }`
  - `chunk` → data `{ text, index }`
  - `done` → data `{}`
  - `error` → data `{ message }`

## Nginx

Ensure proxy buffering is disabled for SSE and HTTP/1.1 is used:

```nginx
location /api/ {
  proxy_http_version 1.1;
  proxy_set_header Connection "";
  proxy_buffering off;
  proxy_cache off;
  chunked_transfer_encoding on;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_pass http://backend:3003/api;
}
```

The repository already includes this configuration under `nginx/default.conf`.

## Tenant Header

Multi-tenancy relies on the `X-Updraft-Tenant` header (e.g., `localdev.localhost`).
Frontend sends this automatically. For manual calls, include:

```bash
# Example curl header
-H "X-Updraft-Tenant: localdev.localhost"
```

## Timeouts and Retries

- Default stream timeout can be tuned via `LLM_STREAM_TIMEOUT_S` (backend env).
- Provider retries/backoff are controlled by `LLM_RETRY_ATTEMPTS` and `LLM_RETRY_BACKOFF_S`.
