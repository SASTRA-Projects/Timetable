import importlib

__version__ = "0.1.1a1"

__all__ = ["mysql_connector", "add_data", "insert_data", "show_data", "fetch_data", "delete_data"]

def __getattr__(name):
    if name in __all__:
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__} has no attribute {name}")
