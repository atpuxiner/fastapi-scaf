import traceback

from fastapi import APIRouter, Depends

from app.api.response import Response, response_docs
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
_active = True  # 激活(若省略则默认True)


# 注意：`user`仅为模块示例，请根据自身需求修改
# 注意：`user`仅为模块示例，请根据自身需求修改
# 注意：`user`仅为模块示例，请根据自身需求修改


@user_router.get(
    path="/user/{user_id}",
    summary="user详情",
    responses=response_docs(
        model=GetUserBiz,
    ),
)
async def get(
        user_id: str,
        current_user: JWTUser = Depends(get_current_user),  # 认证
):
    try:
        user_biz = GetUserBiz(id=user_id)
        data = await user_biz.get()
        if not data:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="user详情失败", error=e)
    return Response.success(data=data)


@user_router.get(
    path="/user",
    summary="user列表",
    responses=response_docs(
        model=GetUserListBiz,
        is_list=True,
        is_total=True,
    ),
)
async def get_list(
        page: int = 1,
        size: int = 10,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = GetUserListBiz(page=page, size=size)
        data, total = await user_biz.get_list()
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="user列表失败", error=e)
    return Response.success(data={"data": data, "total": total})


@user_router.post(
    path="/user",
    summary="user创建",
    responses=response_docs(data={
        "id": "str",
    }),
)
async def create(
        user_biz: CreateUserBiz,
):
    try:
        user_id = await user_biz.create()
        if not user_id:
            return Response.failure(msg="用户已存在", status=Status.RECORD_EXISTS_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="user创建失败", error=e)
    return Response.success(data={"id": user_id})


@user_router.put(
    path="/user/{user_id}",
    summary="user更新",
    responses=response_docs(data={
        "id": "str",
    }),
)
async def update(
        user_id: str,
        user_biz: UpdateUserBiz,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        updated_ids = await user_biz.update(user_id)
        if not updated_ids:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="user更新失败", error=e)
    return Response.success(data={"id": user_id})


@user_router.delete(
    path="/user/{user_id}",
    summary="user删除",
    responses=response_docs(data={
        "id": "str",
    }),
)
async def delete(
        user_id: str,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        user_biz = DeleteUserBiz()
        deleted_ids = await user_biz.delete(user_id)
        if not deleted_ids:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="user删除失败", error=e)
    return Response.success(data={"id": user_id})


@user_router.post(
    path="/user/login",
    summary="userLogin",
    responses=response_docs(data={
        "token": "str",
    }),
)
async def login(
        user_biz: LoginUserBiz,
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
        user_biz: TokenUserBiz,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        data = await user_biz.token()
        if not data:
            return Response.failure(msg="用户不存在", status=Status.UNAUTHORIZED_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="userToken失败", error=e)
    return Response.success(data={"token": data})
