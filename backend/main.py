from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from api import (
    router as ai_router,
    validation_exception_handler,
    rate_limit_exception_handler,
)
from api.tables import router as tables_router
from api.admin import router as admin_router
from core.ratelimit import limiter


app = FastAPI(title="Campus Elad Software")

# CORS configuration - allows frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# Include routers
app.include_router(ai_router, prefix="/api/v1")
app.include_router(tables_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
