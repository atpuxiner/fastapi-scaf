"""
路由
"""
import importlib

from fastapi import FastAPI

from app import APP_DIR

API_MOD_DIR = APP_DIR.joinpath("api")
API_MOD_PREFIX = "app.api"
API_PREFIX = "/api"


def register_default_router(app: FastAPI, mod_str: str = "default", obj_suffix: str = "_router"):
    """
    注册默认路由
    """
    mod_obj = importlib.import_module(f"{API_MOD_PREFIX}.{mod_str}")
    mod_obj_str = f"{mod_str}{obj_suffix}"
    router = getattr(mod_obj, mod_obj_str)
    app.include_router(router, prefix=API_PREFIX, tags=[mod_str])


def register_routers_dynamically(app: FastAPI, api_version: str = "v1", obj_suffix: str = "_router"):
    """
    动态注册路由
    要求：
        路由模块：搜索非'__'开头的模块
        路由对象：{模块名称}{后缀}
    :param app: FastAPI实例
    :param api_version: api版本
    :param obj_suffix: 对象后缀
    :return:
    """
    curr_api_prefix = f"{API_PREFIX}/{api_version}".rstrip("/")
    for f in API_MOD_DIR.joinpath(api_version).glob("*.py"):
        if not f.name.startswith("__"):
            mod_str = f.name[:-3]
            mod_obj = importlib.import_module(f"{API_MOD_PREFIX}.{api_version}.{mod_str}")
            mod_obj_str = f"{mod_str}{obj_suffix}"
            if not hasattr(mod_obj, mod_obj_str):
                continue
            router = getattr(mod_obj, mod_obj_str)
            app.include_router(router, prefix=curr_api_prefix, tags=[mod_str])
