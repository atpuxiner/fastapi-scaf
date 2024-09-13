import traceback

from fastapi import APIRouter, Depends

from app.api.response import Response
from app.business.tpl import (
    GetTplBiz,
)
from app.initializer import g
from app.middleware.auth import JWTUser, get_current_user

tpl_router = APIRouter()


@tpl_router.get("/tpl/{tpl_id}", summary="tpl详情")
async def get(
        tpl_id: int,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        tpl_biz = GetTplBiz(tpl_id=tpl_id)
        data = await tpl_biz.get()
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="tpl详情失败", error=e)
    return Response.success(data=data)
