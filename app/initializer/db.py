import asyncio
import importlib

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

from app import APP_DIR

_DATATYPE_MOD_DIR = APP_DIR.joinpath("datatype")
_DATATYPE_MOD_PREFIX = "app.datatype"

_is_tables_created = False


def init_db(
        db_url: str,
        db_echo: bool,
        db_pool_size: int = 10,
        db_max_overflow: int = 5,
        db_pool_recycle: int = 3600,
        is_create_tables: bool = True,
) -> scoped_session:
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

    def create_tables():
        from app.datatype import DeclBase
        _import_tables()
        try:
            DeclBase.metadata.create_all(engine)
        except (
                exc.OperationalError,
                exc.IntegrityError,
                exc.ProgrammingError,
        ) as e:
            if "already exists" in str(e):
                pass
            else:
                raise

    global _is_tables_created
    if is_create_tables and not _is_tables_created:
        create_tables()
        _is_tables_created = True

    return scoped_session(db_session)


def init_db_async(
        db_url: str,
        db_echo: bool,
        db_pool_size: int = 10,
        db_max_overflow: int = 5,
        db_pool_recycle: int = 3600,
        is_create_tables: bool = True,
) -> sessionmaker:
    db_echo = db_echo or False
    kwargs = {
        "pool_size": db_pool_size,
        "max_overflow": db_max_overflow,
        "pool_recycle": db_pool_recycle,
    }
    if db_url.startswith("sqlite"):
        kwargs = {}
    async_engine = create_async_engine(
        url=db_url,
        echo=db_echo,
        echo_pool=db_echo,
        **kwargs,
    )
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)  # noqa

    async def create_tables():
        from app.datatype import DeclBase
        _import_tables()
        async with async_engine.begin() as conn:
            try:
                await conn.run_sync(DeclBase.metadata.create_all)
            except (
                    exc.OperationalError,
                    exc.IntegrityError,
                    exc.ProgrammingError,
            ) as e:
                if "already exists" in str(e):
                    pass
                else:
                    raise

    global _is_tables_created
    if is_create_tables and not _is_tables_created:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        task = loop.create_task(create_tables())
        task.add_done_callback(lambda t: t.result() if not t.cancelled() else None)
        if not loop.is_running():
            loop.run_until_complete(task)
        _is_tables_created = True
    return async_session


def _import_tables():
    """导入表"""
    for f in _DATATYPE_MOD_DIR.glob("*.py"):
        if not f.name.startswith("__"):
            _ = importlib.import_module(f"{_DATATYPE_MOD_PREFIX}.{f.stem}")
