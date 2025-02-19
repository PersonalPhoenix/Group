from fastapi import (
    FastAPI,
)

from app.users.endpoints.api_v1.api_v1_router import (
    router as api_v1_router,
)

app = FastAPI(
    title='Mini-Chat',
)


app.include_router(
    router=api_v1_router,
)
