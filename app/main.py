from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import AppException

from app.routers.user import router as user_router
from app.routers.category import router as category_router
from app.routers.supplier import router as supplier_router
from app.routers.product import router as product_router
from app.routers.stock_movement import router as stock_movement_router

app = FastAPI()

app.include_router(user_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(stock_movement_router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": err["loc"][-1] if err["loc"] else "unknown",
            "message": err["msg"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )