from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "answer": "השאלה ארוכה מדי (מקסימום 150 תווים). אנא נסה לקצר.",
            "category": "VALIDATION_ERROR",
        },
    )


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "answer": "יותר מדי בקשות. אנא נסה שוב בעוד דקה.",
            "category": "RATE_LIMIT_ERROR",
        },
    )
