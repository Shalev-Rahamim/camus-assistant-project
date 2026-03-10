from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from api.routes import router as ai_router
from api.exceptions import validation_exception_handler
from core.ratelimit import limiter

app = FastAPI(title="Smart Campus Assistant")
app.state.limiter = limiter
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(ai_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "up and running"}
