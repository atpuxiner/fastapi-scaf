"""
路由
"""
import importlib
import sys

from fastapi import FastAPI

from app import APP_DIR

API_MOD_DIR = APP_DIR.joinpath("api")
API_MOD_PREFIX = "app.api"


def register_routers(
        app: FastAPI,
        subdirs: list = None
):
    """
    注册路由
    要求：
        路由模块：搜索非'__'开头的模块
        路由对象：{模块名称}{后缀}
    :param app: 应用
    :param subdirs: 子目录
    :return:
    """
    if not subdirs:
        subdirs = [subdir for subdir in API_MOD_DIR.rglob('*') if subdir.is_dir() and subdir.stem != "__pycache__"]
    for subdir in subdirs:
        subdir_str = subdir.stem
        subdir_obj = importlib.import_module(f"{API_MOD_PREFIX}.{subdir_str}")
        prefix = ""
        if hasattr(subdir_obj, "_prefix"):
            prefix = getattr(subdir_obj, "_prefix")
        register_routers_by_subdir(
            app,
            subdir=subdir_str,
            prefix=prefix,
        )


def register_routers_by_subdir(
        app: FastAPI,
        subdir: str,
        prefix: str = "",
        router_suffix: str = "_router",
):
    """
    注册路由
    要求：
        路由模块：搜索非'__'开头的模块
        路由对象：{模块名称}{后缀}
    :param app: 应用
    :param subdir: 子目录
    :param prefix: 前缀，如：/api/v1
    :param router_suffix: 路由后缀
    :return:
    """
    prefix = prefix.rstrip("/")
    for f in API_MOD_DIR.joinpath(subdir).glob("*.py"):
        if not f.name.startswith("__"):
            mod_str = f.stem
            _mod_obj = f"{API_MOD_PREFIX}.{subdir}.{mod_str}"
            mod_obj = importlib.import_module(_mod_obj)
            mod_obj_str = f"{mod_str}{router_suffix}"
            if hasattr(mod_obj, mod_obj_str):
                router = getattr(mod_obj, mod_obj_str)
                if hasattr(mod_obj, "_active") and not getattr(mod_obj, "_active"):
                    sys.modules.pop(_mod_obj)
                    continue
                app.include_router(router, prefix=prefix, tags=[mod_str])
