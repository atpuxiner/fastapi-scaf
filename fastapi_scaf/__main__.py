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
    )
    parser.add_argument("command", choices=["new", "add"], help="[必填]创建项目或添加api")
    parser.add_argument("target", help="[必填]项目或api名称(多个api可英文逗号分隔)")
    parser.add_argument("api_version", nargs='?', default="v1", const="v1", help="[可选]api版本(默认v1)")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    cmd = CMD(args)
    if args.command == "new":
        cmd.new()
    else:
        cmd.add()


class CMD:

    def __init__(self, args):
        args.target = args.target.replace(" ", "")
        if not args.target:
            sys.stderr.write(f"{prog}: target cannot be empty\n")
            sys.exit(1)
        if args.command == "new":
            if not re.search(r"^[a-zA-Z][a-zA-Z0-9_]{0,64}$", args.target):
                sys.stderr.write(f"{prog}: target contains invalid characters\n")
                sys.exit(1)
        else:
            for t in args.target.strip(",").split(","):
                if not re.search(r"^[a-zA-Z][a-zA-Z0-9_]{0,64}$", t):
                    sys.stderr.write(f"{prog}: target contains invalid characters\n")
                    sys.exit(1)
            args.api_version = args.api_version.replace(" ", "")
            if not args.api_version:
                sys.stderr.write(f"{prog}: api_version cannot be empty\n")
                sys.exit(1)
            if not re.search(r"^v[a-zA-Z0-9_]{0,10}$", args.api_version):
                sys.stderr.write(f"{prog}: api_version contains invalid characters\n")
                sys.exit(1)
        self.args = args

    def new(self):
        sys.stdout.write("Starting new project...\n")
        target = Path(self.args.target)
        if target.is_dir() and any(target.iterdir()):
            sys.stderr.write(f"{prog}: '{target}' exists\n")
            sys.exit(1)
        target.mkdir(parents=True, exist_ok=True)
        with open(here.joinpath("_project_tpl.json"), "r") as f:
            project = json.loads(f.read())
        for k, v in project.items():
            sf = target.joinpath(k)
            sf.parent.mkdir(parents=True, exist_ok=True)
            with open(sf, "w+", encoding="utf-8") as f:
                if k.endswith("README.md"):
                    v = v.replace("# fastapi-scaf", "# fastapi-scaf ( => yourProj)")
                f.write(v)
        sys.stdout.write("Done\n")

    def add(self):
        target = self.args.target
        need_mods = [
            "app/api/vn/",
            "app/business/",
            "app/datatype/",
        ]
        work_dir = Path.cwd()

        def check_mod(t_):
            for mod_ in need_mods:
                curr_mod_dir = work_dir.joinpath(mod_.replace("vn", self.args.api_version))
                if not curr_mod_dir.is_dir():
                    curr_mod_dir = curr_mod_dir.as_posix().replace(work_dir.as_posix(), "").lstrip("/")
                    sys.stderr.write(f"[error] not exists: {curr_mod_dir}\n")
                    sys.exit(1)
                curr_mod_path = curr_mod_dir.joinpath(t_ + ".py")
                if curr_mod_path.is_file():
                    curr_mod_path = curr_mod_path.as_posix().replace(work_dir.as_posix(), "").lstrip("/")
                    return f"already exists: {curr_mod_path}\n"

        def get_api_tpl():
            with open(here.joinpath("_api_tpl.json"), "r", encoding="utf-8") as f:
                return json.loads(f.read())

        api_tpl = {}
        for t in target.strip(",").split(","):
            sys.stdout.write(f"Adding api:\n")
            if e := check_mod(t):
                sys.stderr.write(f"[{t}] {e}")
                continue
            if not api_tpl:
                api_tpl = get_api_tpl()
            for mod in need_mods:
                curr_mod = mod.replace("vn", self.args.api_version) + t + ".py"
                with open(work_dir.joinpath(curr_mod), "w+", encoding="utf-8") as f:
                    sys.stdout.write(f"[{t}] Writing {curr_mod}\n")
                    v = api_tpl[mod.replace("/", "_") + "tpl.py"]
                    f.write(v.replace("tpl", t).replace("Tpl", t.title()))


if __name__ == "__main__":
    main()
