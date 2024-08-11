"""
中间件
"""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.api.exception import CustomException
from app.middleware.cors import Cors
from app.middleware.exception import ExceptionHandler


def register_middlewares(app: FastAPI):
    """注册中间件"""
    app.add_middleware(
        middleware_class=Cors.middleware_class,
        allow_origins=Cors.allow_origins,
        allow_credentials=Cors.allow_credentials,
        allow_methods=Cors.allow_methods,
        allow_headers=Cors.allow_headers,
    )

    app.add_exception_handler(CustomException, ExceptionHandler.custom_exception_handler)  # type: ignore
    app.add_exception_handler(HTTPException, ExceptionHandler.http_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, ExceptionHandler.validation_exception_handler)  # type: ignore
