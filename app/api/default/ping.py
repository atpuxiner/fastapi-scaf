from fastapi import APIRouter

ping_router = APIRouter()
_active = True  # 激活状态


@ping_router.get(
    path="/ping",
    summary="ping",
)
def ping():
    return "pong"
