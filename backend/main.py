import importlib

from starlette.middleware.cors import CORSMiddleware

from backend.config import (
    settings,
)
from backend.custom_types import (
    App,
)


def get_app(path_to_app: str, app_name: str) -> App:
    module = importlib.import_module(path_to_app)

    return getattr(module, app_name)


backend = get_app(
    path_to_app=settings.PATH_TO_APP,
    app_name=settings.APP_NAME,
)

backend.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app default URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"]  # Allows all headers
)
