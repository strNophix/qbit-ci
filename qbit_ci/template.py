import os

from jinja2 import BaseLoader
from jinja2 import Environment

MNT_PREFIX = os.getenv("MNT_PREFIX", ".tmp")

def real_path(path: str):
    return os.path.join(MNT_PREFIX, path[1:])

def path_exists(path: str):
    return os.path.exists(path)

template_env = Environment(loader=BaseLoader())
template_env.filters["real_path"] = real_path
template_env.filters["path_exists"] = path_exists

__all__ = ("real_path", "path_exists", "template_env")
