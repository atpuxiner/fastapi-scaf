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
    initializer,
    router,
    middleware,
)

app = FastAPI()

initializer.g.setup()
router.register_default_router(app)
router.register_routers_dynamically(app, api_version='v1')
middleware.register_middlewares(app)
