"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract main
@description
@history
"""
from fastapi import FastAPI

from app import (
    router,
    middleware,
)
from app.initializer import g

app = FastAPI()

g.setup()
g.logger.info(f"Using yaml '{g.conf.yamlname}'")
# #
router.register_routers(app)
middleware.register_middlewares(app)
