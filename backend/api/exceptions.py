from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "answer": "השאלה ארוכה מדי (מקסימום 150 תווים). אנא נסה לקצר.",
            "category": "VALIDATION_ERROR",
        },
    )
