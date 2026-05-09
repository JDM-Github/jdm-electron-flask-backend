import sys
import os
import eventlet
eventlet.monkey_patch()

def resource_path(relative_path):
    """Resolve paths correctly whether running as script or PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

os.environ.setdefault("FLASK_ENV", "production")
from app import create_app, socketio
from app.utils.printer import Printer

static_folder = resource_path("static")
app = create_app(config_name="production", static_folder=static_folder)
port = int(os.environ.get("FLASK_PORT", 5000))

Printer.log("=" * 50)
Printer.log("Production server starting...")
Printer.log(f"Environment: {app.config.get('FLASK_ENV', 'production')}")
Printer.log(f"Serving on http://127.0.0.1:{port}")
Printer.log("Press Ctrl+C to stop")
Printer.log("=" * 50)

socketio.run(app, host="0.0.0.0", port=port, debug=False)