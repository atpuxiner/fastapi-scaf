"""
初始化
"""
from loguru._logger import Logger  # noqa
from sqlalchemy.orm import sessionmaker
from toollib.guid import SnowFlake
from toollib.redis_cli import RedisCli
from toollib.utils import Singleton

from app.initializer.conf import init_conf
from app.initializer.db import init_db_async
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

    def setup(self):
        """
        初始化
        """
        self.conf = init_conf()
        self.logger = init_logger(
            debug=self.conf.debug,
            log_dir=self.conf.log_dir,
        )
        self.db_async = init_db_async(
            db_async_url=self.conf.db_async_url,
            db_echo=self.conf.debug,
            db_url=self.conf.db_url,
        )
        self.redis = init_redis(
            host=self.conf.redis_host,
            port=self.conf.redis_port,
            db=self.conf.redis_db,
        )
        self.snow = init_snow(
            worker_id=self.conf.snow_worker_id,
            datacenter_id=self.conf.snow_datacenter_id,
        )


g = G()
# 建议：
# 为了避免G下的全局变量在未初始化时使用，
# 请使用以下方式调用：g.conf.xxx
# 而不是在模块预先定义全局变量再调用
# <<< 建议
