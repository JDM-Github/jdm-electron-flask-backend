# Flask Backend Template

Generic Flask backend template designed to pair with the `npx jdm-create-flask-electron` frontend. Serves a React build as a SPA and exposes a JSON REST API.

---

## Project Structure

```
flask-template/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── config.py            # Config classes (Dev / Prod)
│   │
│   ├── api/                 # HTTP layer — blueprints only, no business logic
│   │   ├── health.py        # GET /api/health
│   │   └── example.py       # Your feature endpoints (rename/copy this)
│   │
│   ├── core/                # Business logic — no Flask imports here
│   │   └── service.py       # do_something(), do_something_batch()
│   │
│   ├── models/              # Data models, sample datasets, schemas
│   │   └── __init__.py
│   │
│   └── utils/               # Shared helpers
│       ├── responses.py     # success() / error() response helpers
│       └── validators.py    # @validate_json() decorator
│
├── run.py                   # Dev server entry point
├── production_run.py        # Production (waitress) + PyInstaller entry point
├── requirements.txt
└── .env.example
```

---

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in your env
cp .env.example .env

# 3. Run dev server
python run.py
```

---

## Adding a New Feature

### 1. Create your API blueprint

Copy `app/api/example.py` → `app/api/myfeature.py` and rename the blueprint:

```python
myfeature_bp = Blueprint("myfeature", __name__, url_prefix="/api/myfeature")
```

### 2. Create your core service

Copy `app/core/service.py` → `app/core/myfeature_service.py` and implement your logic inside `do_something()` and `do_something_batch()`.

### 3. Register the blueprint

In `app/__init__.py`:

```python
from app.api.myfeature import myfeature_bp
app.register_blueprint(myfeature_bp)
```

That's it.

---

## API Conventions

### Success response
```json
{
  "success": true,
  "message": "Processed successfully",
  "data": { ... }
}
```

### Error response
```json
{
  "success": false,
  "message": "Missing fields: input",
  "details": "..."   // optional
}
```

### `@validate_json` decorator

Ensures `Content-Type: application/json` and that required fields exist. The decorated function receives the parsed `data` dict as its first argument:

```python
@bp.route("/endpoint", methods=["POST"])
@validate_json("field_a", "field_b")
def endpoint(data):
    value = data["field_a"]
    ...
```

---

## Configuration

All config lives in `app/config.py`. Add your env vars to `Config` (shared) or to `DevelopmentConfig` / `ProductionConfig` as needed.

| Variable          | Default       | Description                     |
|-------------------|---------------|---------------------------------|
| `SECRET_KEY`      | `change-me`   | Flask secret key                |
| `MAX_WORKERS`     | `2`           | ThreadPoolExecutor worker count |
| `REQUEST_TIMEOUT` | `60`          | External HTTP timeout (seconds) |
| `FLASK_ENV`       | `development` | `development` or `production`   |

---

## Production / Electron

```bash
python production_run.py
```

- Uses `waitress` (no dev server)
- Resolves `static/` correctly inside a PyInstaller bundle (`sys._MEIPASS`)
- Loads `.env` from both the bundle root and the CWD

Place your React build output in `static/` before bundling.

---

## Endpoints

| Method | Path                       | Description                  |
|--------|----------------------------|------------------------------|
| GET    | `/api/health`              | Global health check          |
| POST   | `/api/example/process`     | Process a single item        |
| POST   | `/api/example/process/batch` | Process a list of items    |
| GET    | `/api/example/health`      | Feature-level health check   |

Replace `example` with your feature name as you build out the app.
