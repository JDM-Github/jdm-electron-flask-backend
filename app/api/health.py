from flask import Blueprint
from app.utils.responses import success
from app.utils.validators import require_access

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
@require_access
def health():
    return success({"status": "ok"}, "Service is running")