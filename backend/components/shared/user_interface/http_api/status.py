from flask import Blueprint, jsonify

status_blueprint = Blueprint("status", __name__)


# Not exposed by "api" which means this is an internal endpoint not exposed via Cloudfront
@status_blueprint.get("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200
