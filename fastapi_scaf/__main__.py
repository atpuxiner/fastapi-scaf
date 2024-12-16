"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract main
@description
@history
"""
import argparse
import json
import re
import sys
from pathlib import Path

from . import __version__

here = Path(__file__).absolute().parent

prog = "fastapi-scaf"


def main():
    parser = argparse.ArgumentParser(
        prog=prog,
        description="fastapi脚手架，一键生成项目或api，让开发变得更简单",
        epilog="examples: \n"
               "  `new`: %(prog)s new myproj --db=postgresql\n"
               "  `add`: %(prog)s add myapi",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "command",
        choices=["new", "add"],
        help="创建项目或添加api")
    parser.add_argument(
        "name",
        type=str,
        help="项目或api名称(多个api可英文逗号分隔)")
    parser.add_argument(
        "--db",
        default="sqlite",
        choices=["sqlite", "mysql", "postgresql"],
        metavar="",
        help="`new`时可指定项目数据库(默认sqlite)")
    parser.add_argument(
        "--vn",
        type=str,
        default="v1",
        metavar="",
        help="`add`时可指定api版本号(默认v1)")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    cmd = CMD(args)
    if args.command == "new":
        cmd.new()
    else:
        cmd.add()


class CMD:

    def __init__(self, args):
        args.name = args.name.replace(" ", "")
        if not args.name:
            sys.stderr.write(f"{prog}: name cannot be empty\n")
            sys.exit(1)
        if args.command == "new":
            if not re.search(r"^[a-zA-Z][a-zA-Z0-9_]{0,64}$", args.name):
                sys.stderr.write(f"{prog}: name contains invalid characters\n")
                sys.exit(1)
        else:
            for t in args.name.strip(",").split(","):
                if not re.search(r"^[a-zA-Z][a-zA-Z0-9_]{0,64}$", t):
                    sys.stderr.write(f"{prog}: name contains invalid characters\n")
                    sys.exit(1)
            args.vn = args.vn.replace(" ", "")
            if not args.vn:
                sys.stderr.write(f"{prog}: vn cannot be empty\n")
                sys.exit(1)
            if not re.search(r"^v[a-zA-Z0-9_]{0,10}$", args.vn):
                sys.stderr.write(f"{prog}: vn contains invalid characters\n")
                sys.exit(1)
        self.args = args

    def new(self):
        sys.stdout.write("Starting new project...\n")
        name = Path(self.args.name)
        if name.is_dir() and any(name.iterdir()):
            sys.stderr.write(f"{prog}: '{name}' exists\n")
            sys.exit(1)
        name.mkdir(parents=True, exist_ok=True)
        with open(here.joinpath("_project_tpl.json"), "r") as f:
            project = json.loads(f.read())
        for k, v in project.items():
            tplpath = name.joinpath(k)
            tplpath.parent.mkdir(parents=True, exist_ok=True)
            with open(tplpath, "w+", encoding="utf-8") as f:
                # # rpl
                if re.search(r"README\.md$", k):
                    v = v.replace("# fastapi-scaf", "# fastapi-scaf ( => yourProj)")
                if re.search(r"requirements\.txt$", k):
                    _default = self._db_requirements_map("default")
                    _user = self._db_requirements_map(self.args.db) or _default
                    v = v.replace(
                        _default,
                        '\n'.join(_user)
                    )
                if _env := re.search(r"app_(.*?).yaml$", k):
                    _rpl_name = f"/app_{_env.group(1)}"
                    _default = self._db_yaml_map("default")
                    _user = self._db_yaml_map(self.args.db) or _default
                    v = v.replace(
                        _default["db_url"].replace("/app_dev", _rpl_name),
                        _user["db_url"].replace("/app_dev", _rpl_name)
                    ).replace(
                        _default["db_async_url"].replace("/app_dev", _rpl_name),
                        _user["db_async_url"].replace("/app_dev", _rpl_name)
                    )
                # ##
                f.write(v)
        sys.stdout.write("Done\n")

    @staticmethod
    def _db_requirements_map(name: str):
        return {
            "default": "aiosqlite~=0.20.0",
            "sqlite": [
                "aiosqlite~=0.20.0",
            ],
            "mysql": [
                "PyMySQL~=1.1.1",
                "aiomysql~=0.2.0",
            ],
            "postgresql": [
                "psycopg2-binary~=2.9.10",
                "asyncpg~=0.30.0",
            ],
        }.get(name)

    @staticmethod
    def _db_yaml_map(name: str):
        return {
            "default": {
                "db_url": "db_url: sqlite:///app_dev.sqlite",
                "db_async_url": "db_async_url: sqlite+aiosqlite:///app_dev.sqlite",
            },
            "sqlite": {
                "db_url": "db_url: sqlite:///app_dev.sqlite",
                "db_async_url": "db_async_url: sqlite+aiosqlite:///app_dev.sqlite",
            },
            "mysql": {
                "db_url": "db_url: mysql+pymysql://<username>:<password>@<host>:<port>/app_dev?charset=utf8mb4",
                "db_async_url": "db_async_url: mysql+aiomysql://<username>:<password>@<host>:<port>/app_dev?charset=utf8mb4",
            },
            "postgresql": {
                "db_url": "db_url: postgresql://<username>:<password>@<host>:<port>/app_dev",
                "db_async_url": "db_async_url: postgresql+asyncpg://<username>:<password>@<host>:<port>/app_dev",
            },
        }.get(name)

    def add(self):
        name = self.args.name
        need_mods = [
            "app/api/vn/",
            "app/business/",
            "app/datatype/",
        ]
        work_dir = Path.cwd()

        def check_mod(n_):
            for mod_ in need_mods:
                curr_mod_dir = work_dir.joinpath(mod_.replace("vn", self.args.vn))
                if not curr_mod_dir.is_dir():
                    curr_mod_dir = curr_mod_dir.as_posix().replace(work_dir.as_posix(), "").lstrip("/")
                    sys.stderr.write(f"[error] not exists: {curr_mod_dir}\n")
                    sys.exit(1)
                curr_mod_path = curr_mod_dir.joinpath(n_ + ".py")
                if curr_mod_path.is_file():
                    curr_mod_path = curr_mod_path.as_posix().replace(work_dir.as_posix(), "").lstrip("/")
                    return f"already exists: {curr_mod_path}\n"

        def get_api_tpl():
            with open(here.joinpath("_api_tpl.json"), "r", encoding="utf-8") as f:
                return json.loads(f.read())

        api_tpl = {}
        for n in name.strip(",").split(","):
            sys.stdout.write(f"Adding api:\n")
            if e := check_mod(n):
                sys.stderr.write(f"[{n}] {e}")
                continue
            if not api_tpl:
                api_tpl = get_api_tpl()
            for mod in need_mods:
                curr_mod = mod.replace("vn", self.args.vn) + n + ".py"
                with open(work_dir.joinpath(curr_mod), "w+", encoding="utf-8") as f:
                    sys.stdout.write(f"[{n}] Writing {curr_mod}\n")
                    v = api_tpl[mod.replace("/", "_") + "tpl.py"]
                    f.write(v.replace("tpl", n).replace("Tpl", n.title()))


if __name__ == "__main__":
    main()
