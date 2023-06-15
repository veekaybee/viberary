import importlib.resources
from io import TextIOWrapper
from pathlib import Path

def get_resource(resource)-> TextIOWrapper:
    with importlib.resources.as_file(resource) as path:
        f = path.open()
        return f
    


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent
