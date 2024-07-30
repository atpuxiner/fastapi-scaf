import subprocess


def main():
    cmd = (
        'uvicorn main:app '
        '--host=0.0.0.0 '
        '--port=8000 '
        '--log-level=debug '
        '--log-config=../config/uvicorn_logging.json '
        '--reload'
    )
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    main()
