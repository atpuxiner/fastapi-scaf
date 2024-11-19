# fastapi-scaf

## What is this?

- by: axiner
- fastapi-scaf
- This is a fastapi scaf.
    - new project
    - add api
    - about project:
        - auto init project (conf, db, logger...)
        - auto register router
        - auto register middleware

## Project Structure

- ABD: ABD模式
    - A api
    - B business
    - D datatype
- 调用过程: main.py(initializer) - router(middleware) - api - business - (datatype)
- 结构如下: (命名经过多次修改敲定，简洁易懂，ABD目录贴合避免杂乱无章)
  ```
  └── fastapi-scaf
      ├── app                         (应用)
      │   ├── api                     ├── (api)
      │   │   └── v1                  │   └── (v1)
      │   ├── business                ├── (业务)
      │   ├── datatype                ├── (数据类型)
      │   ├── initializer             ├── (初始化)
      │   │   ├── conf                │   ├── (配置)
      │   │   ├── db                  │   ├── (数据库)
      │   │   ├── logger              │   ├── (日志)
      │   │   └── ...                 │   └── (...)
      │   ├── middleware              ├── (中间件)
      │   ├── router                  ├── (路由)
      │   ├── utils                   ├── (utils)
      │   └── main.py                 └── (main.py)
      ├── config                      (配置目录)
      ├── deploy                      (部署目录)
      ├── docs                        (文档目录)
      ├── log                         (日志目录)
      ├── .gitignore
      ├── LICENSE
      ├── README.md
      └── requirements.txt
  ```

## Installation

This package can be installed using pip (>=Python3.11):
> pip install fastapi-scaf

## Scaf Usage

- 1）new project
    - `fastapi-scaf new <project_name>`
- 2）add api
    - `cd to project root dir`
    - `fastapi-scaf add <api_name>`

## Project Run

- 1）cd to project root dir
- 2）execute command:
    - `pip install -r requirements.txt`
    - `uvicorn app.main:app --host=0.0.0.0 --port=8000 --log-level=debug --log-config=./config/uvicorn_logging.json --workers=5`
    - about uvicorn: [www.uvicorn.org](https://www.uvicorn.org/)

## LICENSE

This project is released under the MIT License (MIT). See [LICENSE](LICENSE)
