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

here = Path(__file__).absolute().parent

prog = "fastapi-scaf"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["new", "add"], help="new project or add api")
    parser.add_argument("target", help="project or api name")
    parser.add_argument("--version", default="v1", help="api version")
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
        if not re.search(r"^[a-zA-Z][a-zA-Z0-9_]{0,64}$", args.target):
            sys.stderr.write(f"{prog}: target contains invalid characters\n")
            sys.exit(1)
        if args.command == "add":
            args.version = args.version.replace(" ", "")
            if not args.version:
                sys.stderr.write(f"{prog}: version cannot be empty\n")
                sys.exit(1)
            if not re.search(r"^v[a-zA-Z0-9_]{0,10}$", args.version):
                sys.stderr.write(f"{prog}: version contains invalid characters\n")
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

    def add(self):
        sys.stdout.write("Starting add api...\n")
        target = self.args.target
        need_mods = [
            "app/api/vn/",
            "app/business/",
            "app/datatype/",
        ]
        work_dir = Path.cwd()
        for m in need_mods:
            curr_mod_dir = work_dir.joinpath(m.replace("vn", self.args.version))
            if not curr_mod_dir.is_dir():
                curr_mod_dir = curr_mod_dir.as_posix().replace(work_dir.as_posix(), "").lstrip("/")
                sys.stderr.write(f"{prog}: '{curr_mod_dir}' not exists\n")
                sys.exit(1)
            curr_mod_py = curr_mod_dir.joinpath(target + ".py")
            if curr_mod_py.is_file():
                curr_mod_py = curr_mod_py.as_posix().replace(work_dir.as_posix(), "").lstrip("/")
                sys.stderr.write(f"{prog}: '{curr_mod_py}' exists\n")
                sys.exit(1)
        with open(here.joinpath("_api_tpl.json"), "r") as f:
            api = json.loads(f.read())
        for m in need_mods:
            curr_m = work_dir.joinpath(m.replace("vn", self.args.version) + target + ".py")
            with open(curr_m, "w+", encoding="utf-8") as f:
                v = api[m.replace("/", "_") + "tpl.py"]
                f.write(v.replace("tpl", target).replace("Tpl", target.title()))


if __name__ == "__main__":
    main()
