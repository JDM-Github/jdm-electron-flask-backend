"""API blueprints package."""
from .example import ExampleBlueprint
from .health import HealthBlueprint

__all__ = ["ExampleBlueprint", "HealthBlueprint"]