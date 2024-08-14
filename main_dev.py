"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract main_dev（开发用）
@description
@history
"""
import argparse


def run_by_cmd():
    import subprocess

    cmd = (
        'uvicorn app.main:app '
        '--host=0.0.0.0 '
        '--port=8000 '
        '--log-level=debug '
        '--log-config=./config/uvicorn_logging.json '
        '--reload'
    )
    subprocess.run(cmd, shell=True)


def run_by_uvicorn():
    import uvicorn
    from app.main import app

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        log_config="./config/uvicorn_logging.json"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", action='store_true', help="是否cmd运行")
    args = parser.parse_args()
    is_cmd = args.cmd
    if is_cmd:
        run_by_cmd()
    else:
        run_by_uvicorn()


if __name__ == '__main__':
    main()
