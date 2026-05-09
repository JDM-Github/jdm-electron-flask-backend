from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from app.config import DevelopmentConfig, ProductionConfig, DeployedConfig
from app.utils.printer import Printer
import importlib
import json
import os

socketio = SocketIO()

def load_blueprints(app, env):
    api_config_path = os.path.join(os.path.dirname(__file__), "..", "config", "api.json")
    with open(api_config_path, "r") as f:
        api_config = json.load(f)

    for name, config in api_config.items():
        if not config.get("masterEnabled", True):
            Printer.warn(f"[{name}] skipped (masterEnabled: false)")
            continue
        if env == "production" and config.get("disabledOnProduction", False):
            Printer.warn(f"[{name}] skipped (disabledOnProduction: true)")
            continue
        if env == "deployed" and config.get("disabledOnDeployed", False):
            Printer.warn(f"[{name}] skipped (disabledOnDeployed: true)")
            continue

        try:
            module = importlib.import_module(f"app.api.{name}")
            blueprint = getattr(module, f"{name}_bp")
            app.register_blueprint(blueprint, url_prefix=config["link"])
            Printer.success(f"[{name}] registered at {config['link']}")
        except ModuleNotFoundError as e:
            if f"app.api.{name}" in str(e):
                Printer.error(f"[{name}] module app/api/{name}.py not found — skipped")
            else:
                Printer.error(f"[{name}] failed to import — missing dependency: {e}")
        except AttributeError:
            Printer.error(f"[{name}] blueprint '{name}_bp' not found in module — skipped")
        except Exception as e:
            Printer.error(f"[{name}] unexpected error — {e}")

def create_app(config_name=None, static_folder="static"):
    app = Flask(__name__, static_folder=static_folder, static_url_path="/static")
    CORS(app, origins="*")

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    if config_name == "production":
        app.config.from_object(ProductionConfig)
    elif config_name == "deployed":
        app.config.from_object(DeployedConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    Printer.init(config_name)
    Printer.info(f"Environment: {config_name}")

    # ---- SocketIO ----
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="eventlet",
        logger=config_name == "development",
        engineio_logger=config_name == "development",
    )
    from app.event import connect
    # ------------------

    Printer.log("\n  Registering blueprints...\n")
    load_blueprints(app, config_name)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app