import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import current_app
from jdm_electron_flask import Printer
class ExampleService:

    @staticmethod
    def process_item(item: str) -> dict:
        start = time.time()
        try:
            result_value = item.upper()
            elapsed = time.time() - start
            result = {
                "input": item,
                "result": result_value,
                "elapsed": round(elapsed, 4),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            Printer.success(f"Processed item: {item}")
            return result
        except Exception as e:
            Printer.error(f"Failed processing item '{item}': {str(e)}")
            return {
                "input": item,
                "result": None,
                "elapsed": 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(e),
            }

    @staticmethod
    def process_batch(items: list[str], max_workers: int = None) -> list[dict]:
        max_workers = max_workers or current_app.config.get("MAX_WORKERS", 2)
        Printer.info(f"Starting batch processing ({len(items)} items)")

        results = [None] * len(items)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(ExampleService.process_item, item): idx
                for idx, item in enumerate(items)
            }

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    results[idx] = future.result()
                except Exception as exc:
                    Printer.error(
                        f"Batch processing failed for item "
                        f"'{items[idx]}': {str(exc)}"
                    )
                    results[idx] = {
                        "input": items[idx],
                        "result": None,
                        "elapsed": 0,
                        "timestamp": time.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "error": str(exc),
                    }

        Printer.success("Batch processing completed")
        return results
