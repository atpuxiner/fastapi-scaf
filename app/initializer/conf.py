import os

import yaml
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

from app import APP_DIR

CONFIG_DIR = APP_DIR.parent.joinpath("config")
ENV_PATH = os.environ.setdefault("ENV_PATH", str(CONFIG_DIR.joinpath(".env")))
load_dotenv(dotenv_path=ENV_PATH)
YAML_NAME = f"app_{os.environ.setdefault('appenv', 'dev')}.yaml"
YAML_PATH = CONFIG_DIR.joinpath(YAML_NAME)
if not YAML_PATH.exists():
    raise RuntimeError(f"YAML配置不存在：{YAML_PATH}")


class Conf(BaseSettings):
    """配置"""
    yaml_name: str = YAML_NAME
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
        _()
        # 特殊配置：比如设置默认值、类型转换或其他操作
        # 如：self.foo = _("foo", "foo")
        # <<< 特殊配置
        self.yaml_conf = dict()
        return self

    def conf_from_yaml(self, name: str = None, default=None):
        if not self.yaml_conf:
            self.yaml_conf = self.load_yaml()
            for k, v in self.yaml_conf.items():  # auto
                setattr(self, k, v)
        return self.yaml_conf.get(name, default)

    def load_yaml(self):
        with open(self.yaml_path or str(YAML_PATH), mode='r', encoding='utf-8') as file:
            return yaml.safe_load(file)


def init_conf() -> Conf:
    return Conf().setup()
