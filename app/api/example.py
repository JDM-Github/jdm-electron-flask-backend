from jdm_electron_flask import JDMBlueprint, success, error
from app.core.example_service import ExampleService

class ExampleBlueprint(JDMBlueprint):
    def __init__(self):
        super().__init__("example", __name__)

    @JDMBlueprint.post("/process", auth=True, validate="input")
    def process_single(data):
        item = data["input"]
        if not isinstance(item, str) or not item.strip():
            return error("'input' must be a non-empty string", 400)
        return success(ExampleService.process_item(item), "Processed successfully")

    @JDMBlueprint.post("/process/batch", auth=True, validate="inputs")
    def process_batch(data):
        items = data["inputs"]
        if not isinstance(items, list) or not items:
            return error("'inputs' must be a non-empty list", 400)
        results = ExampleService.process_batch(items)
        return success({"results": results}, f"Processed {len(results)} items")

    @JDMBlueprint.get("/health", auth=False)
    def health():
        return success({"status": "ok"}, "Service is running")
