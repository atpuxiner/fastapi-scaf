"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract main
@description
@history
"""
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app import (
    router,
    middleware,
)
from app.initializer import g

logger = logging.getLogger("uvicorn")

g.setup()
# #
openapi_url = "/openapi.json"
docs_url = "/docs"
redoc_url = "/redoc"
if g.conf.is_disable_docs is True:
    openapi_url, docs_url, redoc_url = None, None, None


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info(f"Using config file '{g.conf.yamlname}'")
    logger.info(f"App name '{g.conf.appname}'")
    logger.info(f"App version '{g.conf.appversion}'")
    yield


app = FastAPI(
    title=g.conf.appname,
    version=g.conf.appversion,
    debug=g.conf.debug,
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    lifespan=lifespan,
)
# #
router.register_routers(app)
middleware.register_middlewares(app)
