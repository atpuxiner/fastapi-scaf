from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.exception import CustomException
from app.api.response import JSONFailure
from app.api.status import Status


class ExceptionHandler:

    @staticmethod
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        return JSONFailure(msg=exc.msg, code=exc.code, data=exc.data)

    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONFailure(msg=exc.detail, code=exc.status_code)

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONFailure(
            msg=", ".join([f"'{item['loc'][1] if len(item['loc']) > 1 else item['loc'][0]}' {item['msg'].lower()}" for item in exc.errors()]),  # noqa: E501
            status=Status.PARAMS_ERROR,
        )
