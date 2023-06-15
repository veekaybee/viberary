import importlib.resources
from io import TextIOWrapper

def get_resource(resource)-> TextIOWrapper:
    with importlib.resources.as_file(resource) as path:
            with path.open() as f:
                return f