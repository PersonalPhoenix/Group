import importlib

from app.config import (
    settings,
)
from app.custom_types import (
    App,
)


def get_app(path_to_app: str, app_name: str) -> App:
    module = importlib.import_module(path_to_app)

    return getattr(module, app_name)


app = get_app(
    path_to_app=settings.PATH_TO_APP,
    app_name=settings.APP_NAME,
)
