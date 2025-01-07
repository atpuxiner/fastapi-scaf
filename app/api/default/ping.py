from fastapi import APIRouter

ping_router = APIRouter()
_active = True  # 激活(若省略则默认True)


@ping_router.get(
    path="/ping",
    summary="ping",
)
def ping():
    return "pong"
