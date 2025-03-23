from fastapi import (
    FastAPI,
)

from backend.endpoints.api_v1.api_v1_router import (
    router as api_v1_router,
)

backend = FastAPI(
    title='Mini-Chat',
)


backend.include_router(
    router=api_v1_router,
)
