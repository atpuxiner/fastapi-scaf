import traceback

from fastapi import APIRouter, Depends

from app.api.response import Response, response_docs
from app.api.status import Status
from app.business.user import (
    UserDetailBiz,
    UserListBiz,
    UserCreateBiz,
    UserUpdateBiz,
    UserDeleteBiz,
    UserLoginBiz,
    UserTokenBiz,
)
from app.initializer import g
from app.middleware.auth import JWTUser, get_current_user

user_router = APIRouter()
_active = True  # 激活状态（默认激活）
_tag = "user"  # 标签（默认模块名或子目录名）


# 注意：`user`仅为模块示例，请根据自身需求修改
# 注意：`user`仅为模块示例，请根据自身需求修改
# 注意：`user`仅为模块示例，请根据自身需求修改


@user_router.get(
    path="/user/{user_id}",
    summary="userDetail",
    responses=response_docs(
        model=UserDetailBiz,
    ),
)
async def detail(
        user_id: str,
        current_user: JWTUser = Depends(get_current_user),  # 认证
):
    try:
        user_biz = UserDetailBiz(id=user_id)
        data = await user_biz.detail()
        if not data:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userDetail失败", error=e)
    return Response.success(data=data)


@user_router.get(
    path="/user",
    summary="userList",
    responses=response_docs(
        model=UserListBiz,
        is_listwrap=True,
        listwrap_key="items",
        listwrap_key_extra={
            "total": "int",
        },
    ),
)
async def lst(
        page: int = 1,
        size: int = 10,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = UserListBiz(page=page, size=size)
        data, total = await user_biz.lst()
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userList失败", error=e)
    return Response.success(data={"items": data, "total": total})


@user_router.post(
    path="/user",
    summary="userCreate",
    responses=response_docs(data={
        "id": "str",
    }),
)
async def create(
        user_biz: UserCreateBiz,
):
    try:
        user_id = await user_biz.create()
        if not user_id:
            return Response.failure(msg="用户已存在", status=Status.RECORD_EXISTS_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userCreate失败", error=e)
    return Response.success(data={"id": user_id})


@user_router.put(
    path="/user/{user_id}",
    summary="userUpdate",
    responses=response_docs(data={
        "id": "str",
    }),
)
async def update(
        user_id: str,
        user_biz: UserUpdateBiz,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        updated_ids = await user_biz.update(user_id)
        if not updated_ids:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userUpdate失败", error=e)
    return Response.success(data={"id": user_id})


@user_router.delete(
    path="/user/{user_id}",
    summary="userDelete",
    responses=response_docs(data={
        "id": "str",
    }),
)
async def delete(
        user_id: str,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = UserDeleteBiz()
        deleted_ids = await user_biz.delete(user_id)
        if not deleted_ids:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userDelete失败", error=e)
    return Response.success(data={"id": user_id})


@user_router.post(
    path="/user/login",
    summary="userLogin",
    responses=response_docs(data={
        "token": "str",
    }),
)
async def login(
        user_biz: UserLoginBiz,
):
    try:
        data = await user_biz.login()
        if not data:
            return Response.failure(msg="用户名或密码错误", status=Status.UNAUTHORIZED_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userLogin失败", error=e)
    return Response.success(data={"token": data})


@user_router.post(
    path="/user/token",
    summary="userToken",
    responses=response_docs(data={
        "token": "str",
    }),
)
async def token(
        user_biz: UserTokenBiz,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        data = await user_biz.token()
        if not data:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userToken失败", error=e)
    return Response.success(data={"token": data})
