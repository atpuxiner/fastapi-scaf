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
        return f"{self.msg}[{self.code}]"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.code!r}, msg={self.msg!r})"


class UnauthorizedError(CustomException):

    def __init__(
            self,
            msg: str = None,
            code: int = None,
            data: Any = None,
            status: Status = Status.UNAUTHORIZED_ERROR,
    ):
        super().__init__(msg, code, data, status)
