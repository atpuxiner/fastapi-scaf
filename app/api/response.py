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
            headers: Mapping[str, str] | None = None,
            media_type: str | None = None,
            background: BackgroundTask | None = None,
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
            headers: Mapping[str, str] | None = None,
            media_type: str | None = None,
            background: BackgroundTask | None = None,
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


def response_docs(
        model=None,  # 模型（从模型的`response_fields`方法获取字段并解析）
        data: dict = None,  # 数据（传值则不从模型中解析）
        is_list: bool = False,
        is_total: bool = False,
        appends: dict = None,
):
    """响应文档"""

    def _data_from_model(model_) -> dict:
        """数据模板"""
        data_ = {}
        if hasattr(model_, "response_fields"):
            all_fields = set(model_.response_fields())
        else:
            all_fields = set(model_.model_fields.keys())
        for field_name in all_fields:
            data_[field_name] = model_.model_fields[field_name].annotation.__name__
        return data_

    if not data and model:
        data = _data_from_model(model)
    if is_list:
        data = data if isinstance(data, list) else [data]
    if is_total:
        data = {
            "data": data,
            "total": "int"
        }
    docs = {
        0: {
            "description": "操作成功",
            "content": {
                "application/json": {
                    "example": {
                        "time": "时间戳",
                        "msg": "消息",
                        "code": "为0",
                        "data": data
                    }
                }
            }
        },
        1: {
            "description": "操作失败",
            "content": {
                "application/json": {
                    "example": {
                        "time": "时间戳",
                        "msg": "消息",
                        "code": "非0",
                        "error": "异常消息",
                        "data": "额外数据",
                    }
                }
            }
        },
    }
    if appends:
        docs.update(appends)
    docs.update({  # 覆盖默认的
        200: {
            "description": "[弃用]",
        },
        422: {
            "description": "[弃用]",
        },
    })
    return docs
