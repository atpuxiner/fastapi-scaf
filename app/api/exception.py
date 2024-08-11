from typing import Any

from app.api.status import Status


class CustomException(Exception):

    def __init__(
            self,
            msg: str = None,
            code: int = None,
            data: Any = None,
            status: Status = Status.FAILURE,
    ):
        self.msg = msg or status.msg
        self.code = code or status.code
        self.data = data
        self.status = status

    def __str__(self) -> str:
        return f"{self.code}: {self.msg}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.code!r}, msg={self.msg!r})"


class ParamsError(CustomException):

    def __init__(
            self,
            msg: str = None,
            code: int = None,
            data: Any = None,
            status: Status = Status.PARAMS_ERROR,
    ):
        super().__init__(msg, code, data, status)


class UnauthorizedError(CustomException):

    def __init__(
            self,
            msg: str = None,
            code: int = None,
            data: Any = None,
            status: Status = Status.UNAUTHORIZED_ERROR,
    ):
        super().__init__(msg, code, data, status)
