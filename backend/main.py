from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from api import (
    router as ai_router,
    validation_exception_handler,
    rate_limit_exception_handler,
)
from core.ratelimit import limiter


app = FastAPI(title="Smart Campus Assistant")
app.state.limiter = limiter
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
app.include_router(ai_router, prefix="/api/v1")
