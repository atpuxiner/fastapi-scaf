from fastapi import APIRouter

ping_router = APIRouter()


@ping_router.get(
    path="/ping",
    summary="ping",
)
def ping():
    return "pong"
