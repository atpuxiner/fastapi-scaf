import os

import yaml
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

from app import APP_DIR

CONFIG_DIR = APP_DIR.parent.joinpath("config")
ENV_PATH = os.environ.setdefault("ENV_PATH", str(CONFIG_DIR.joinpath(".env")))
YAML_PATH = CONFIG_DIR.joinpath("app.yaml")
# load env
load_dotenv(dotenv_path=ENV_PATH)


class Conf(BaseSettings):
    """配置"""
    yaml_conf: dict = None

    # +++++++++ env中配置 +++++++++
    yaml_path: str = None

    # +++++++++ 初始中配置 +++++++++
    debug: bool = None
    log_dir: str = None
    # #
    db_url: str = None
    db_async_url: str = None
    redis_host: str = None
    redis_port: int = None
    redis_db: int = None
    snow_worker_id: int = None
    snow_datacenter_id: int = None

    def setup(self, func_name: str = "conf_from_yaml"):
        _ = getattr(self, func_name)
        # 配置：
        self.debug = _("debug", False)
        self.log_dir = _("log_dir", "")
        # #
        self.db_url = _("db_url")
        self.db_async_url = _("db_async_url")
        self.redis_host = _("redis_host")
        self.redis_port = _("redis_port")
        self.redis_db = _("redis_db")
        self.snow_worker_id = _("snow_worker_id", 0)
        self.snow_datacenter_id = _("snow_datacenter_id", 0)
        # <<< 配置
        self.yaml_conf = dict()
        return self

    def conf_from_yaml(self, name: str, default=None):
        if not self.yaml_conf:
            self.yaml_conf = self.load_yaml()
        return self.yaml_conf.get(name, default)

    def load_yaml(self):
        with open(self.yaml_path or str(YAML_PATH), 'r') as file:
            return yaml.safe_load(file)


def init_conf() -> Conf:
    return Conf().setup()
