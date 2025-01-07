import json
import re
from pathlib import Path

from toollib.utils import listfile

project_dir = Path(__file__).absolute().parent.parent.parent


def gen_project_json():
    include_mods_comp = re.compile('|'.join([
        "app",
        "config",
        "deploy",
        "docs",
        "log",
        ".gitignore",
        "LICENSE",
        "main_dev.py",
        "README.md",
        "requirements.txt",
    ]))
    exclude_exts_comp = re.compile('|'.join([
        ".pyc$",
        ".log$",
        ".sqlite3?$",
    ]))
    data = {}
    for file in listfile(project_dir, is_r=True):
        file_str = file.as_posix().replace(project_dir.as_posix(), "").lstrip("/")
        if include_mods_comp.search(file_str.split("/")[0]) and not exclude_exts_comp.search(file_str):
            with open(file, "r", encoding="utf-8") as f:
                data[file_str] = f.read()
    with open(project_dir.joinpath("fastapi_scaf/_project_tpl.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def gen_api_json():
    data = {}
    _api_tpl = project_dir.joinpath("fastapi_scaf/mgr/_api_tpl")
    for file in listfile(_api_tpl):
        with open(file, "r", encoding="utf-8") as f:
            data[file.name] = f.read()
    with open(project_dir.joinpath("fastapi_scaf/_api_tpl.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run():
    gen_project_json()
    gen_api_json()


if __name__ == '__main__':
    run()
