"""
初始化
"""
from loguru._logger import Logger  # noqa
from sqlalchemy.orm import sessionmaker
from toollib.guid import SnowFlake
from toollib.redis_cli import RedisCli
from toollib.utils import Singleton

from app.initializer.conf import init_conf
from app.initializer.db import init_db_async, db_create_tables_dynamically
from app.initializer.logger import init_logger
from app.initializer.redis import init_redis
from app.initializer.snow import init_snow


class G(metaclass=Singleton):
    """
    全局变量
    """
    conf = None
    logger: Logger = None
    db_async: sessionmaker = None
    redis: RedisCli = None
    snow: SnowFlake = None


def setup():
    """
    初始化
    """
    g.conf = init_conf()
    g.logger = init_logger(debug=g.conf.debug, log_dir=g.conf.log_dir)
    g.db_async = init_db_async(db_async_url=g.conf.db_async_url, db_echo=g.conf.db_echo)
    db_create_tables_dynamically(db_url=g.conf.db_url, db_echo=g.conf.db_echo)
    g.redis = init_redis(host=g.conf.redis_host, port=g.conf.redis_port, db=g.conf.redis_db)
    g.snow = init_snow(worker_id=g.conf.worker_id, datacenter_id=g.conf.datacenter_id)


g = G()
# 为了避免G下的全局变量在未初始化时使用，
# 建议以下方式调用：g.conf.xxx
# 而不是在模块预先定义全局变量再调用
