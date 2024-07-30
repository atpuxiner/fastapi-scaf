import os

import yaml
from dotenv import load_dotenv

from app import APP_DIR

CONFIG_DIR = APP_DIR.parent.joinpath("config")
ENV_PATH = os.environ.setdefault("ENV_PATH", str(CONFIG_DIR.joinpath(".env")))
YAML_PATH = CONFIG_DIR.joinpath("app.yaml")


class BaseConf:
    debug: bool
    log_dir: str
    db_echo: bool
    worker_id: int
    datacenter_id: int


class Conf(BaseConf):
    """conf"""

    # TODO: 配置显性设置
    db_url: str
    db_async_url: str
    redis_host: str
    redis_port: int
    redis_db: int

    def __init__(self):
        super().__init__()
        self.load_env()
        yaml_conf = self.load_yaml()

        # TODO: 配置显性设置
        self.debug = yaml_conf.get("debug", False)
        self.log_dir = yaml_conf.get("log_dir", "")
        self.db_echo = yaml_conf.get("db_echo", False)
        self.worker_id = yaml_conf.get("worker_id", 0)
        self.datacenter_id = yaml_conf.get("datacenter_id", 0)
        # #
        self.db_url = yaml_conf.get("db_url")
        self.db_async_url = yaml_conf.get("db_async_url")
        self.redis_host = yaml_conf.get("redis_host")
        self.redis_port = yaml_conf.get("redis_port")
        self.redis_db = yaml_conf.get("redis_db")

    @staticmethod
    def load_env():
        load_dotenv(dotenv_path=ENV_PATH)

    @staticmethod
    def load_yaml():
        yaml_path = os.environ.setdefault("YAML_PATH", str(YAML_PATH))
        with open(yaml_path, 'r') as file:
            yaml_conf = yaml.safe_load(file)
            return yaml_conf


def init_conf() -> Conf:
    return Conf()
