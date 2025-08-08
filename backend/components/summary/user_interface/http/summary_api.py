from uuid import UUID
from flask import Blueprint, Response, stream_with_context, request, jsonify, g
import json, time, os
from components.summary.user_interface.bus import bus_factory
from components.summary.domain import commands
from components.shared.user_interface.utils import parse_with_for_http
from components.summary.user_interface.http import schemas
from components.summary.application.summary_service import SummaryService
from components.summary.application.providers import ProviderStreamError
from components.shared.infrastructure.errors import NoConfigForTenant

summary_blueprint = Blueprint("summary", __name__, url_prefix="/api/documents")
DATA_PREFIX = "data: "
EVENT_OPEN = "event: open\n"
EVENT_CHUNK = "event: chunk\n"
EVENT_DONE = "event: done\n"
EVENT_ERROR = "event: error\n"


def _map_provider_error_message(err: Exception) -> str:
    msg = str(err) if err else ""
    low = msg.lower()
    if any(
        k in low
        for k in ["api key", "permission", "unauthorized", "forbidden", "invalid key"]
    ):
        return "Provider authentication or permission error. Check API key and tenant configuration."
    if any(k in low for k in ["quota", "rate", "429", "resourceexhausted", "exceeded"]):
        return "Provider is rate limited or quota exceeded. Please retry shortly."
    if any(k in low for k in ["timeout", "deadline", "unavailable", "temporarily"]):
        return "Provider temporarily unavailable. Please retry."
    return "Summarization failed. Please try again."


@summary_blueprint.post("/<uuid:document_id>/summary/stream")
def stream_summary(document_id: UUID):
    options = request.get_json(silent=True) or {}
    bus = bus_factory()
    req_id = getattr(g, "request_id", None)
    bus.logger.info(
        "summary_stream_start",
        extra={"document_id": str(document_id), "request_id": req_id},
    )

    start_time = time.time()
    try:
        timeout_default = int(os.getenv("LLM_STREAM_TIMEOUT_S", "120"))
    except (ValueError, TypeError):
        timeout_default = 120
    opt_timeout = options.get("timeout_s")
    try:
        timeout_s = int(opt_timeout) if opt_timeout is not None else timeout_default
    except (ValueError, TypeError):
        timeout_s = timeout_default

    def event_stream():
        yield EVENT_OPEN
        yield DATA_PREFIX + json.dumps(
            {"document_id": str(document_id), "request_id": req_id}
        ) + "\n\n"
        try:
            provider_stream = SummaryService.generate_stream(
                document_id, options, bus.uow, bus.logger
            )
            for idx, chunk in enumerate(provider_stream):
                if (time.time() - start_time) > timeout_s:
                    yield EVENT_ERROR
                    yield DATA_PREFIX + json.dumps(
                        {"message": "stream timeout"}
                    ) + "\n\n"
                    bus.logger.warning(
                        "summary_stream_timeout",
                        extra={"document_id": str(document_id), "request_id": req_id},
                    )
                    return
                payload = {"text": chunk, "index": idx}
                yield EVENT_CHUNK
                yield DATA_PREFIX + json.dumps(payload) + "\n\n"
            yield EVENT_DONE
            yield DATA_PREFIX + "{}\n\n"
            bus.logger.info(
                "summary_stream_done",
                extra={"document_id": str(document_id), "request_id": req_id},
            )
        except NoConfigForTenant as e:
            bus.logger.warning(
                "summary_stream_no_tenant_config",
                extra={
                    "document_id": str(document_id),
                    "request_id": req_id,
                    "error": str(e),
                },
            )
            yield EVENT_ERROR
            yield DATA_PREFIX + json.dumps(
                {
                    "message": "Tenant not configured for AI provider. Set GEMINI_API_KEY or tenant secrets."
                }
            ) + "\n\n"
        except ProviderStreamError as e:
            # Known provider-side error
            bus.logger.error(
                "summary_stream_provider_error",
                extra={
                    "document_id": str(document_id),
                    "request_id": req_id,
                    "error": str(e),
                },
            )
            yield EVENT_ERROR
            yield DATA_PREFIX + json.dumps(
                {"message": _map_provider_error_message(e)}
            ) + "\n\n"
        except Exception as e:
            # Unexpected error surface as generic message
            bus.logger.exception(
                "summary_stream_unhandled_error",
                extra={"document_id": str(document_id), "request_id": req_id},
            )
            yield EVENT_ERROR
            yield DATA_PREFIX + json.dumps(
                {"message": "Unexpected error. Please try again."}
            ) + "\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream",
        "X-Accel-Buffering": "no",
    }
    return Response(stream_with_context(event_stream()), headers=headers)


@summary_blueprint.get("/<uuid:document_id>/summary")
def get_summary(document_id: UUID):
    bus = bus_factory()
    with bus.uow as uow:
        doc = uow.repositories.documents.get(document_id)
        if not doc:
            from components.documents.application.errors import DocumentNotFound

            raise DocumentNotFound(document_id)
        return (
            jsonify(
                {"document_id": str(document_id), "summary_html": doc.summary_html}
            ),
            200,
        )


@summary_blueprint.post("/<uuid:document_id>/summary")
@parse_with_for_http(schemas.SaveSummaryRequest)
def save_summary(document_id: UUID, payload: schemas.SaveSummaryRequest):
    bus = bus_factory()
    bus.handle(
        commands.SaveSummary(document_id=document_id, content_html=payload.content_html)
    )
    return "OK", 201


@summary_blueprint.put("/<uuid:document_id>/summary")
@parse_with_for_http(schemas.UpdateSummaryRequest)
def update_summary(document_id: UUID, payload: schemas.UpdateSummaryRequest):
    bus = bus_factory()
    bus.handle(
        commands.UpdateSummary(
            document_id=document_id, content_html=payload.content_html
        )
    )
    return "OK", 200


@summary_blueprint.delete("/<uuid:document_id>/summary")
def delete_summary(document_id: UUID):
    bus = bus_factory()
    bus.handle(commands.DeleteSummary(document_id=document_id))
    return "OK", 204
