from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import logger
from app.models.error import ErrorResponse
from app.services.errors import ConflictError, NotFoundError, ServiceError, ValidationError

SERVICE_ERROR_STATUS = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
    ValidationError: status.HTTP_400_BAD_REQUEST,
}

SERVICE_ERROR_CODES = {
    NotFoundError: "not_found",
    ConflictError: "conflict",
    ValidationError: "validation_error",
}

HTTP_STATUS_CODES = {
    status.HTTP_400_BAD_REQUEST: "bad_request",
    status.HTTP_401_UNAUTHORIZED: "unauthorized",
    status.HTTP_403_FORBIDDEN: "forbidden",
    status.HTTP_404_NOT_FOUND: "not_found",
    status.HTTP_409_CONFLICT: "conflict",
    status.HTTP_422_UNPROCESSABLE_CONTENT: "request_validation_error",
}


def _ensure_trace_id(request: Request) -> str:
    trace_id = getattr(request.state, "trace_id", None)
    if trace_id is None:
        trace_id = str(uuid4())
        request.state.trace_id = trace_id
    return trace_id


def _with_trace_header(response: JSONResponse, trace_id: str) -> JSONResponse:
    response.headers.setdefault("X-Request-ID", trace_id)
    return response


def _response(status_code: int, payload: ErrorResponse, trace_id: str) -> JSONResponse:
    return _with_trace_header(
        JSONResponse(status_code=status_code, content=jsonable_encoder(payload)), trace_id
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def handle_service_error(request: Request, exc: ServiceError) -> JSONResponse:
        status_code = SERVICE_ERROR_STATUS.get(type(exc), status.HTTP_400_BAD_REQUEST)
        code = SERVICE_ERROR_CODES.get(type(exc), "service_error")
        trace_id = _ensure_trace_id(request)
        payload = ErrorResponse(code=code, message=str(exc), detail=None, trace_id=trace_id)
        return _response(status_code=status_code, payload=payload, trace_id=trace_id)

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        trace_id = _ensure_trace_id(request)
        detail = None if isinstance(exc.detail, str) else jsonable_encoder(exc.detail)
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        code = HTTP_STATUS_CODES.get(exc.status_code, "http_error")
        payload = ErrorResponse(code=code, message=message, detail=detail, trace_id=trace_id)
        return _response(status_code=exc.status_code, payload=payload, trace_id=trace_id)

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        trace_id = _ensure_trace_id(request)
        payload = ErrorResponse(
            code="request_validation_error",
            message="Request validation failed",
            detail=jsonable_encoder(exc.errors()),
            trace_id=trace_id,
        )
        return _response(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            payload=payload,
            trace_id=trace_id,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        trace_id = _ensure_trace_id(request)
        logger.exception("Unhandled application error", exc_info=exc, extra={"trace_id": trace_id})
        payload = ErrorResponse(
            code="internal_error",
            message="An unexpected error occurred",
            detail=None,
            trace_id=trace_id,
        )
        return _response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, payload=payload, trace_id=trace_id
        )
