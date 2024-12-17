import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

from app import APP_DIR

CONFIG_DIR = APP_DIR.parent.joinpath("config")

load_dotenv(dotenv_path=os.environ.setdefault(
    key="envpath",
    value=str(CONFIG_DIR.joinpath(".env")))
)
# #
yamlpath = Path(
    os.environ.get("yamlpath") or
    CONFIG_DIR.joinpath(f"app_{os.environ.setdefault(key='appenv', value='dev')}.yaml")
)
if not yamlpath.is_file():
    raise RuntimeError(f"配置文件不存在：{yamlpath}")


class Conf(BaseSettings):
    """配置"""
    yamlname: str = yamlpath.name
    yamlconf: dict = None

    # +++++++++ env中配置 +++++++++

    # +++++++++ 初始中配置 +++++++++
    debug: bool = None
    log_dir: str = None
    # #
    snow_worker_id: int = None
    snow_datacenter_id: int = None
    redis_host: str = None
    redis_port: int = None
    redis_db: int = None
    redis_password: str = None
    db_url: str = None
    db_async_url: str = None

    def setup(self, func_name: str = "conf_from_yaml"):
        _ = getattr(self, func_name)
        _()
        # 特殊配置：比如设置默认值、类型转换或其他操作
        # 如：self.foo = _("foo", "foo")
        # <<< 特殊配置
        self.yamlconf = dict()
        return self

    def conf_from_yaml(self, name: str = None, default=None):
        if not self.yamlconf:
            self.yamlconf = self.load_yaml()
            for k, v in self.yamlconf.items():  # auto
                setattr(self, k, v)
        return self.yamlconf.get(name, default)

    @staticmethod
    def load_yaml():
        with open(yamlpath, mode="r", encoding="utf-8") as file:
            return yaml.safe_load(file)


def init_conf() -> Conf:
    return Conf().setup()
