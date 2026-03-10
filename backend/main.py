from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from api import (
    router as ai_router,
    validation_exception_handler,
    rate_limit_exception_handler,
)
from api.admin.routes import router as admin_courses_router
from core.ratelimit import limiter


app = FastAPI(title="Smart Campus Assistant")
app.state.limiter = limiter
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

# Include routers
app.include_router(ai_router, prefix="/api/v1")
app.include_router(admin_courses_router, prefix="/api/v1")
