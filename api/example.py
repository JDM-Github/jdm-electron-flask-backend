from flask import Blueprint
from app.utils.responses import success, error
from app.utils.validators import validate_json
from app.core.service import do_something, do_something_batch

# Rename this blueprint to match your feature (e.g., "sentiment", "ocr", "chat")
example_bp = Blueprint("example", __name__, url_prefix="/api/example")

# ------------------------------------------------------------------ #
#  Single-item endpoint                                                #
# ------------------------------------------------------------------ #
@example_bp.route("/process", methods=["POST"])
@validate_json("input")
def process_single(data):
    """
    Process a single item.
    Request body: { "input": "<your data>" }
    """
    item = data["input"]
    if not isinstance(item, str) or not item.strip():
        return error("'input' must be a non-empty string", 400)

    result = do_something(item)
    return success(result, "Processed successfully")


# ------------------------------------------------------------------ #
#  Batch endpoint                                                      #
# ------------------------------------------------------------------ #
@example_bp.route("/process/batch", methods=["POST"])
@validate_json("inputs")
def process_batch(data):
    """
    Process a list of items.
    Request body: { "inputs": ["item1", "item2", ...] }
    """
    items = data["inputs"]
    if not isinstance(items, list) or len(items) == 0:
        return error("'inputs' must be a non-empty list of strings", 400)
    for item in items:
        if not isinstance(item, str) or not item.strip():
            return error("Each item must be a non-empty string", 400)

    results = do_something_batch(items)
    return success({"results": results}, f"Processed {len(results)} items")
