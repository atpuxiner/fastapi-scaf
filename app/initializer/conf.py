import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

from app import APP_DIR

_CONFIG_DIR = APP_DIR.parent.joinpath("config")

load_dotenv(dotenv_path=os.environ.setdefault(
    key="envpath",
    value=str(_CONFIG_DIR.joinpath(".env")))
)
# #
appyaml = Path(
    os.environ.get("appyaml") or
    _CONFIG_DIR.joinpath(f"app_{os.environ.setdefault(key='appenv', value='dev')}.yaml")
)
if not appyaml.is_file():
    raise RuntimeError(f"配置文件不存在：{appyaml}")


class Conf(BaseSettings):
    """配置"""
    yamlname: str = appyaml.name
    yamlconf: dict = None

    # +++++++++ env中配置 +++++++++

    # +++++++++ 初始中配置 +++++++++
    appname: str = None
    appversion: str = None
    debug: bool = None
    log_dir: str = None
    is_disable_docs: bool = None
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
        self.appname = _("appname", default="DbyApp")
        self.appversion = _("appversion", default="1.0.0")
        self.debug = _("debug", default=False)
        self.log_dir = _("log_dir", default="./log")
        self.is_disable_docs = _("is_disable_docs", default=True)
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
        with open(appyaml, mode="r", encoding="utf-8") as file:
            return yaml.safe_load(file)


def init_conf() -> Conf:
    return Conf().setup()
