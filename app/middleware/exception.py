from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.exception import CustomException
from app.api.response import Response
from app.api.status import Status


class ExceptionHandler:

    @staticmethod
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        return Response.failure(msg=exc.msg, code=exc.code, data=exc.data)

    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return Response.failure(msg=exc.detail, code=exc.status_code)

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError, is_display_all: bool = False) -> JSONResponse:  # noqa: E501
        if is_display_all:
            msg = ", ".join([f"'{item['loc'][1] if len(item['loc']) > 1 else item['loc'][0]}' {item['msg'].lower()}" for item in exc.errors()])  # noqa: E501
        else:
            _first_error = exc.errors()[0]
            msg = f"'{_first_error['loc'][1] if len(_first_error['loc']) > 1 else _first_error['loc'][0]}' {_first_error['msg'].lower()}"  # noqa: E501
        return Response.failure(
            msg=msg,
            status=Status.PARAMS_ERROR,
        )
