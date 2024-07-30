from typing import Union

from toollib.utils import now2timestamp

from app.api.status import Status


class Response:

    @staticmethod
    def success(
            data: Union[dict, list, str] = None,
            msg: str = None,
            code: int = None,
            status: Status = Status.SUCCESS,
    ):
        return {
            "time": now2timestamp(),
            "msg": msg or status.msg,
            "code": code or status.code,
            "data": data,
        }

    @staticmethod
    def failure(
            msg: str = None,
            code: int = None,
            data: Union[dict, list, str] = None,
            status: Status = Status.FAILURE,
    ):
        return {
            "time": now2timestamp(),
            "msg": msg or status.msg,
            "code": code or status.code,
            "data": data,
        }

    @staticmethod
    def custom(result: dict):
        return result
