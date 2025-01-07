"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract main_dev（开发用）
@description
@history
"""
import argparse
import subprocess

import uvicorn


def run_by_cmd(
        host: str,
        port: int,
        workers: int,
        log_level: str,
        log_config: str,
        is_reload: bool,
):
    cmd = (
        'uvicorn app.main:app '
        '--host={host} '
        '--port={port} '
        '--workers={workers} '
        '--log-level={log_level} '
        '--log-config={log_config} '
        '{reload}'.format(
            host=host,
            port=port,
            workers=workers,
            log_level=log_level,
            log_config=log_config,
            reload=f'--reload' if is_reload else ''
        )
    )
    subprocess.run(cmd, shell=True)


def run_by_mod(
        host: str,
        port: int,
        workers: int,
        log_level: str,
        log_config: str,
        is_reload: bool,
):
    uvicorn.run(
        app="app.main:app",
        host=host,
        port=port,
        workers=workers,
        log_level=log_level,
        log_config=log_config,
        reload=is_reload,
    )


def main(
        host: str,
        port: int,
        workers: int,
        log_level: str,
        log_config: str,
        is_reload: bool,
        is_cmd: bool,
):
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="host")
    parser.add_argument("--port", type=int, help="port")
    parser.add_argument("--workers", type=int, help="进程数")
    parser.add_argument("--log-level", type=str, help="日志等级")
    parser.add_argument("--log-config", type=str, help="日志配置")
    parser.add_argument("--is-reload", action='store_true', help="是否重载")
    parser.add_argument("--is-cmd", action='store_true', help="是否命令行执行")
    args = parser.parse_args()
    kwargs = {
        'host': args.host or host,
        'port': args.port or port,
        'workers': args.workers or workers,
        'log_level': args.log_level or log_level,
        'log_config': args.log_config or log_config,
        'is_reload': args.is_reload or is_reload,
    }
    if args.is_cmd or is_cmd:
        run_by_cmd(**kwargs)
    else:
        run_by_mod(**kwargs)


if __name__ == '__main__':
    main(
        host='0.0.0.0',
        port=8000,
        workers=1,
        log_level='debug',
        log_config='./config/uvicorn_logging.json',
        is_reload=True,
        is_cmd=False,
    )
