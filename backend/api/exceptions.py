from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "answer": "The question is too long (maximum 150 characters). Please shorten it.",
            "category": "VALIDATION_ERROR",
        },
    )


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "answer": "Too many requests. Please try again in a minute.",
            "category": "RATE_LIMIT_ERROR",
        },
    )
