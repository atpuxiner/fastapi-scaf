"""
路由
"""
import importlib

from fastapi import FastAPI

from app import APP_DIR

API_MOD_DIR = APP_DIR.joinpath("api")
API_MOD_PREFIX = "app.api"


def register_routers(
        app: FastAPI,
        api_subdir: str,
        api_prefix: str = "",
        obj_suffix: str = "_router",
):
    """
    注册路由
    要求：
        路由模块：搜索非'__'开头的模块
        路由对象：{模块名称}{后缀}
    :param app: FastAPI实例
    :param api_subdir: api子目录
    :param api_prefix: api前缀，如：/api/v1
    :param obj_suffix: 对象后缀
    :return:
    """
    api_prefix = api_prefix.rstrip("/")
    for f in API_MOD_DIR.joinpath(api_subdir).glob("*.py"):
        if not f.name.startswith("__"):
            mod_str = f.stem
            mod_obj = importlib.import_module(f"{API_MOD_PREFIX}.{api_subdir}.{mod_str}")
            mod_obj_str = f"{mod_str}{obj_suffix}"
            if hasattr(mod_obj, mod_obj_str):
                router = getattr(mod_obj, mod_obj_str)
                app.include_router(router, prefix=api_prefix, tags=[mod_str])
