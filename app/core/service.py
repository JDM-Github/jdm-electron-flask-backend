"""
core/service.py
---------------
Replace this file with your actual business logic.

This module is the heart of your feature. Keep HTTP concerns (Flask, request,
response) OUT of here — this layer should be fully testable without a running
server.

Typical patterns you can follow (all shown below as stubs):
  - Single-item processing  → do_something()
  - Concurrent batch work   → do_something_batch()
  - External API call       → _call_external_api()
  - Scoring / evaluation    → score()
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config import Config


# ------------------------------------------------------------------ #
#  External API helper (adapt or delete)                              #
# ------------------------------------------------------------------ #
def _call_external_api(payload: dict) -> dict:
    """
    Make a request to an external service.
    Returns a parsed result dict, or {"error": "..."} on failure.
    """
    import requests

    headers = {
        # "Authorization": f"Bearer {Config.EXTERNAL_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            # Config.EXTERNAL_API_URL,
            "http://localhost:8000/api/endpoint",  # replace with real URL
            json=payload,
            headers=headers,
            timeout=Config.REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}


# ------------------------------------------------------------------ #
#  Core processing functions                                           #
# ------------------------------------------------------------------ #
def do_something(item: str) -> dict:
    """
    Process a single item and return a result dict.
    Swap out the stub logic for your real implementation.
    """
    start = time.time()

    result_value = item.upper()
    elapsed = time.time() - start
    return {
        "input": item,
        "result": result_value,
        "elapsed": round(elapsed, 4),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

def do_something_batch(items: list, max_workers: int = None) -> list:
    """
    Process many items concurrently.
    Returns a list of result dicts in the original order.
    """
    if max_workers is None:
        max_workers = Config.MAX_WORKERS

    results = [None] * len(items)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(do_something, item): idx
            for idx, item in enumerate(items)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as exc:
                results[idx] = {
                    "input": items[idx],
                    "result": None,
                    "elapsed": 0,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "error": str(exc),
                }
    return results
