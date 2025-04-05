"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract main
@description
@history
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app import (
    router,
    middleware,
)
from app.initializer import g

g.setup()
# #
openapi_url = "/openapi.json"
docs_url = "/docs"
redoc_url = "/redoc"
if g.config.is_disable_docs is True:
    openapi_url, docs_url, redoc_url = None, None, None


@asynccontextmanager
async def lifespan(app_: FastAPI):
    g.logger.info(f"Application using config file '{g.config.yamlname}'")
    g.logger.info(f"Application name '{g.config.appname}'")
    g.logger.info(f"Application version '{g.config.appversion}'")
    # #
    g.logger.info("Application server running")
    yield
    g.logger.info("Application server shutdown")


app = FastAPI(
    title=g.config.appname,
    version=g.config.appversion,
    debug=g.config.debug,
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    lifespan=lifespan,
)
# #
router.register_routers(app)
middleware.register_middlewares(app)
