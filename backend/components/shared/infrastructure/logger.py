import json
import logging
import os
from logging import Formatter, StreamHandler

from flask import g, has_request_context, request
from flask.wrappers import Request


class FlaskUnstructuredFormatter(Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super(FlaskUnstructuredFormatter, self).format(record)
        message_str = record.getMessage()

        msg = "{level} {asctime}".format(level=record.levelname, asctime=record.asctime)

        if has_request_context():
            msg = msg + " x-request-id: {}".format(g.request_id)

        msg = f"{msg} - {message_str}"

        if hasattr(record, "exc_info") and record.exc_info:
            msg = msg + " - stack_trace: {}".format(
                self.formatException(record.exc_info)
            )

        return msg


class FlaskStructuredFormatter(Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super(FlaskStructuredFormatter, self).format(record)
        structured_dict = self._make_structured_dict(record)

        if hasattr(record, "exc_info") and record.exc_info:
            structured_dict["stack_trace"] = self.formatException(record.exc_info)

        if has_request_context():
            structured_dict["metadata"]["context"] = self._get_web_context(g, request)

        return json.dumps(structured_dict, default=str)

    @staticmethod
    def _make_structured_dict(record: logging.LogRecord) -> dict:
        message_str = record.getMessage()

        if isinstance(record.args, dict):
            logger_payload = record.args
        else:
            logger_payload = {"value": repr(record.args)}

        return {
            "message": message_str,
            "logger_payload": logger_payload,
            "metadata": {
                "level": record.levelname,
                "pid": record.process,
                "logger_name": record.name,
                "time": record.asctime,
                "code": {"filename": record.filename, "file_path": record.pathname},
                "context": {"has_web_context": False},
            },
        }

    @staticmethod
    def _get_web_context(app_ctx, flask_request: Request) -> dict:
        return {
            "has_web_context": True,
            "x-request-id": app_ctx.request_id,
            "url": flask_request.url,
            "remote_address": flask_request.remote_addr,
        }


def logger_format_factory():
    if os.getenv("APP_ENV", "production") == "development":
        return FlaskStructuredFormatter(fmt="%(message)s - %(asctime)s")
    else:
        return FlaskUnstructuredFormatter(
            fmt="%(levelname)s - %(asctime)s: %(message)s"
        )


def get_logger():
    _logger = logging.getLogger("updraft-backend")
    if not _logger.handlers:
        logger_level = os.getenv(
            "LOG_LEVEL",
            "WARNING" if os.getenv("APP_ENV", "production") == "production" else "INFO",
        )
        handler = StreamHandler()
        handler.setFormatter(logger_format_factory())
        _logger.addHandler(handler)
        _logger.setLevel(logger_level)
        _logger.propagate = False
    return _logger


logger = get_logger()
