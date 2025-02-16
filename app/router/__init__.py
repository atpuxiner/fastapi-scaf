"""
路由
"""
import importlib
import sys

from fastapi import FastAPI

from app import APP_DIR

_API_MOD_DIR = APP_DIR.joinpath("api")
_API_MOD_PREFIX = "app.api"


def register_routers(
        app: FastAPI,
        subdirs: list = None,
        obj_suffix: str = "_router",
        default_prefix: str = "",
):
    """
    注册路由
    要求：
        路由模块：非'__'开头的模块
        路由对象：{模块名称}{后缀}
    :param app: 应用
    :param subdirs: 子目录
    :param obj_suffix: 对象后缀
    :param default_prefix: 默认前缀
    :return:
    """
    subdirs = subdirs or [d.stem for d in _API_MOD_DIR.rglob('*') if d.is_dir() and d.stem != "__pycache__"]
    for subdir in subdirs:
        subdir_obj = importlib.import_module(f"{_API_MOD_PREFIX}.{subdir}")
        if hasattr(subdir_obj, "_prefix"):
            prefix = getattr(subdir_obj, "_prefix")
        else:
            prefix = default_prefix
        for f in _API_MOD_DIR.joinpath(subdir).glob("*.py"):
            if not f.name.startswith("__"):
                mod_str = f.stem
                _mod_obj = f"{_API_MOD_PREFIX}.{subdir}.{mod_str}"
                mod_obj = importlib.import_module(_mod_obj)
                mod_obj_str = f"{mod_str}{obj_suffix}"
                if hasattr(mod_obj, mod_obj_str):
                    router = getattr(mod_obj, mod_obj_str)
                    if hasattr(mod_obj, "_active") and not getattr(mod_obj, "_active"):
                        sys.modules.pop(_mod_obj)
                        continue
                    app.include_router(
                        router=router,
                        prefix=prefix.rstrip("/"),
                        tags=[mod_str],
                    )
