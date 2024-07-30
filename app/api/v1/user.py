import traceback

from fastapi import APIRouter, Depends

from app.api.exception import ParamsError
from app.api.response import Response
from app.api.status import Status
from app.business.user import (
    GetUserBiz,
    GetUserListBiz,
    CreateUserBiz,
    UpdateUserBiz,
    DeleteUserBiz,
    LoginUserBiz,
    TokenUserBiz,
)
from app.initializer import g
from app.middleware.auth import JWTUser, get_current_user

user_router = APIRouter()


@user_router.get("/user/{user_id}")
async def get(
        user_id: int,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = GetUserBiz(user_id=user_id)
        data = await user_biz.get()
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success(data)


@user_router.get("/user")
async def get_list(
        page: int = 1,
        size: int = 10,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = GetUserListBiz(page=page, size=size)
        data, total = await user_biz.get_list()
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success({"data": data, "total": total})


@user_router.post("/user")
async def create(
        user_biz: CreateUserBiz,
):
    try:
        user_biz.validate_params()
        data = await user_biz.create()
        if not data:
            return Response.failure(msg="用户已存在", status=Status.RECORD_EXISTS_ERROR)
    except ParamsError as e:
        return Response.failure(msg=e.msg, code=e.code, data=e.data)
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success(data)


@user_router.put("/user/{user_id}")
async def update(
        user_id: int,
        user_biz: UpdateUserBiz,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        status = await user_biz.update(user_id)
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success({"id": user_id, "status": status})


@user_router.delete("/user/{user_id}")
async def delete(
        user_id: int,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = DeleteUserBiz()
        status = await user_biz.delete(user_id)
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success({"id": user_id, "status": status})


@user_router.post("/user/login")
async def login(
        user_biz: LoginUserBiz,
):
    try:
        data, msg = await user_biz.login()
        if not data:
            return Response.failure(msg=msg, status=Status.UNAUTHORIZED_ERROR)
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success({"token": data})


@user_router.post("/user/token")
async def token(
        user_biz: TokenUserBiz,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        data, msg = await user_biz.token()
        if not data:
            return Response.failure(msg=msg, status=Status.UNAUTHORIZED_ERROR)
    except Exception as e:
        errmsg = str(e)
        g.logger.error(errmsg)
        g.logger.error(traceback.format_exc())
        return Response.failure(msg=errmsg)
    return Response.success({"token": data})