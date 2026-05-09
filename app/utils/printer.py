import os
import logging
from datetime import datetime


class Printer:

    _logger = None
    _env = None

    @classmethod
    def init(cls, env: str):
        cls._env = env

        if env != "development":
            log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
            os.makedirs(log_dir, exist_ok=True)

            log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
            log_path = os.path.join(log_dir, log_filename)

            logging.basicConfig(
                filename=log_path,
                level=logging.INFO,
                format="%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
            cls._logger = logging.getLogger("app")

    @classmethod
    def log(cls, message: str):
        if cls._env == "development":
            print(message)
        else:
            cls._logger.info(message)

    @classmethod
    def warn(cls, message: str):
        if cls._env == "development":
            print(f"  ⚠  {message}")
        else:
            cls._logger.warning(message)

    @classmethod
    def error(cls, message: str):
        if cls._env == "development":
            print(f"  ✖  {message}")
        else:
            cls._logger.error(message)

    @classmethod
    def success(cls, message: str):
        if cls._env == "development":
            print(f"  ✔  {message}")
        else:
            cls._logger.info(f"[SUCCESS] {message}")

    @classmethod
    def info(cls, message: str):
        if cls._env == "development":
            print(f"  ℹ  {message}")
        else:
            cls._logger.info(f"[INFO] {message}")