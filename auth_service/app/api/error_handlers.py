from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BaseHTTPException

def register_exception_handlers(app: FastAPI):
	@app.exception_handler(BaseHTTPException)
	async def _base_http_exception_handler(_: Request, exc: BaseHTTPException) -> JSONResponse:
		return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
