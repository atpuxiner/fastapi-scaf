from typing import Union, Mapping

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from toollib.utils import now2timestamp

from app.api.status import Status


class Response:

    @staticmethod
    def success(
            data: Union[dict, list, str] = None,
            msg: str = None,
            code: int = None,
            status: Status = Status.SUCCESS,
            status_code: int = 200,
            headers: Mapping[str, str] = None,
            media_type: str = None,
            background: BackgroundTask = None,
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "time": now2timestamp(),
                "msg": msg or status.msg,
                "code": code or status.code,
                "data": data,
            },
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @staticmethod
    def failure(
            msg: str = None,
            code: int = None,
            error: Union[str, Exception] = None,
            data: Union[dict, list, str] = None,
            status: Status = Status.FAILURE,
            status_code: int = 200,
            headers: Mapping[str, str] = None,
            media_type: str = None,
            background: BackgroundTask = None,
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "time": now2timestamp(),
                "msg": msg or status.msg,
                "code": code or status.code,
                "error": str(error),
                "data": data,
            },
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
