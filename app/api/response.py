from typing import Mapping, get_type_hints

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, StreamingResponse, ContentStream
from toollib.utils import now2timestamp, map_jsontype

from app.api.status import Status


class Response:

    @staticmethod
    def success(
            data: dict | list | str | None = None,
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
            error: str | Exception | None = None,
            data: dict | list | str | None = None,
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
                "error": str(error) if error else None,
                "data": data,
            },
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    @staticmethod
    def stream(
            content: ContentStream,
            status_code: int = 200,
            headers: Mapping[str, str] | None = None,
            media_type: str | None = None,
            background: BackgroundTask | None = None,
    ) -> StreamingResponse:
        return StreamingResponse(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


def response_docs(
        model=None,  # 模型(BaseModel): 自动从模型中解析字段与类型
        data: dict | str = None,  # 数据(dict/str): 直接给定字段与类型/类型
        is_listwrap: bool = False,
        listwrap_key: str = None,
        listwrap_key_extra: dict = None,
        docs_extra: dict = None,
):
    """响应文档"""

    def _data_from_model(model_, default: str = "未知") -> dict:
        """数据模板"""
        data_ = {}
        if hasattr(model_, "response_fields"):
            all_fields = set(model_.response_fields())
        else:
            all_fields = set(model_.model_fields.keys())
        type_hints = get_type_hints(model_)
        for field_name in all_fields:
            try:
                t = type_hints.get(field_name)
                t = str(t).replace("<class '", "").replace("'>", "") if t else default
            except Exception:
                t = default
            data_[field_name] = t
        return data_

    full_data = {}
    if model:
        full_data = _data_from_model(model)
    if data:
        if isinstance(data, dict):
            full_data.update(data)
        else:
            full_data = data
    if is_listwrap:
        full_data = [full_data] if not isinstance(full_data, list) else full_data
        if listwrap_key:
            full_data = {listwrap_key: full_data}
            if listwrap_key_extra:
                full_data.update(listwrap_key_extra)

    def _format_value(value):
        if isinstance(value, str):
            _value = value.split("|")
            if len(_value) > 1:
                return " | ".join([map_jsontype(_v.strip(), is_keep_integer=True) for _v in _value])
            return map_jsontype(value, is_keep_integer=True)
        elif isinstance(value, dict):
            return {k: _format_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [_format_value(item) for item in value]
        else:
            return str(value)

    format_data = _format_value(full_data)

    docs = {
        200: {
            "description": "操作成功【code为0 & http状态码200】",
            "content": {
                "application/json": {
                    "example": {
                        "time": "integer",
                        "msg": "string",
                        "code": "integer",
                        "data": format_data
                    }
                }
            }
        },
        422: {
            "description": "操作失败【code非0 & http状态码200】",
            "content": {
                "application/json": {
                    "example": {
                        "time": "integer",
                        "msg": "string",
                        "code": "integer",
                        "error": "string",
                        "data": "object | array | ...",
                    }
                }
            }
        },
    }
    if docs_extra:
        docs.update(docs_extra)
    return docs
