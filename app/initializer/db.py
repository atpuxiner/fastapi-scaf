import importlib

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlmodel import SQLModel

from app import APP_DIR

DATATYPE_MOD_DIR = APP_DIR.joinpath("datatype")
DATATYPE_MOD_PREFIX = "app.datatype"
DEFAULT_DB_URL = f"sqlite:///{APP_DIR.parent.joinpath('app.sqlite3')}"
DEFAULT_DB_ASYNC_URL = f"sqlite+aiosqlite:///{APP_DIR.parent.joinpath('app.sqlite3')}"


def init_db(
        db_url: str,
        db_echo: bool,
        db_pool_size: int = 10,
        db_max_overflow: int = 5,
        db_pool_recycle: int = 3600,
) -> scoped_session:
    db_url = db_url or DEFAULT_DB_URL
    db_echo = db_echo or False
    kwargs = {
        "pool_size": db_pool_size,
        "max_overflow": db_max_overflow,
        "pool_recycle": db_pool_recycle,
    }
    if db_url.startswith("sqlite"):
        kwargs = {}
    engine = create_engine(
        url=db_url,
        echo=db_echo,
        echo_pool=db_echo,
        **kwargs,
    )
    db_session = sessionmaker(engine, expire_on_commit=False)
    return scoped_session(db_session)


def init_db_async(
        db_async_url: str,
        db_echo: bool,
        db_pool_size: int = 10,
        db_max_overflow: int = 5,
        db_pool_recycle: int = 3600,
) -> sessionmaker:
    db_async_url = db_async_url or DEFAULT_DB_ASYNC_URL
    db_echo = db_echo or False
    kwargs = {
        "pool_size": db_pool_size,
        "max_overflow": db_max_overflow,
        "pool_recycle": db_pool_recycle,
    }
    if db_async_url.startswith("sqlite"):
        kwargs = {}
    async_engine = create_async_engine(
        url=db_async_url,
        echo=db_echo,
        echo_pool=db_echo,
        **kwargs,
    )
    async_session_factory = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)  # noqa
    return async_session_factory


def db_create_tables_dynamically(db_url: str, db_echo: bool = False, obj_suffix: str = ""):
    """
    动态创建表
    要求：
        模型模块：搜索非'__'开头的模块
        模型对象：{模块名称}{后缀}
    :param db_url: db url
    :param db_echo: db echo
    :param obj_suffix: 对象后缀
    :return:
    """
    db_echo = db_echo or False
    engine = create_engine(
        url=db_url or DEFAULT_DB_URL,
        echo=db_echo,
        echo_pool=db_echo,
    )
    for f in DATATYPE_MOD_DIR.glob("*.py"):
        if not f.name.startswith("__"):
            mod_str = f.name[:-3]
            mod_obj = importlib.import_module(f"{DATATYPE_MOD_PREFIX}.{mod_str}")
            mod_obj_str = f"{mod_str.title()}{obj_suffix}"
            if not hasattr(mod_obj, mod_obj_str):
                continue
            model: SQLModel = getattr(mod_obj, mod_obj_str)
            model.metadata.create_all(engine)
