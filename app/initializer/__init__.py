"""
初始化
"""
from loguru._logger import Logger  # noqa
from sqlalchemy.orm import sessionmaker, scoped_session
from toollib.guid import SnowFlake
from toollib.redis_cli import RedisCli
from toollib.utils import Singleton

from app.initializer.conf import init_conf
from app.initializer.db import init_db_async, init_db
from app.initializer.logger import init_logger
from app.initializer.redis import init_redis
from app.initializer.snow import init_snow


class G(metaclass=Singleton):
    """
    全局变量
    """
    conf = None
    logger: Logger = None
    snow: SnowFlake = None
    redis: RedisCli = None
    db_session: scoped_session = None
    db_async_session: sessionmaker = None

    def __getattribute__(self, name):
        try:
            value = super().__getattribute__(name)
        except AttributeError:
            value = None
        if value is None:
            getter_name = f"_get_{name}"
            getter_method = getattr(self.__class__, getter_name, None)
            if callable(getter_method):
                value = getter_method()
                setattr(self, name, value)
        return value

    @classmethod
    def _get_conf(cls):
        if not cls.conf:
            cls.conf = init_conf()
        return cls.conf

    @classmethod
    def _get_logger(cls):
        if not cls.logger:
            cls.logger = init_logger(
                debug=cls.conf.debug,
                log_dir=cls.conf.log_dir,
            )
        return cls.logger

    @classmethod
    def _get_snow(cls):
        if not cls.snow:
            cls.snow = init_snow(
                worker_id=cls.conf.snow_worker_id,
                datacenter_id=cls.conf.snow_datacenter_id,
            )
        return cls.snow

    @classmethod
    def _get_redis(cls):
        if not cls.redis:
            cls.redis = init_redis(
                host=cls.conf.redis_host,
                port=cls.conf.redis_port,
                db=cls.conf.redis_db,
                password=cls.conf.redis_password,
            )
        return cls.redis

    @classmethod
    def _get_db_session(cls):
        if not cls.db_session:
            cls.db_session = init_db(
                db_url=cls.conf.db_url,
                db_echo=cls.conf.debug,
            )
        return cls.db_session

    @classmethod
    def _get_db_async_session(cls):
        if not cls.db_async_session:
            cls.db_async_session = init_db_async(
                db_url=cls.conf.db_async_url,
                db_echo=cls.conf.debug,
            )
        return cls.db_async_session

    @classmethod
    def setup(cls):
        """
        初始化
        """
        cls._get_conf()
        cls._get_logger()
        cls._get_snow()
        cls._get_redis()
        # cls._get_db_session()
        cls._get_db_async_session()


g = G()
