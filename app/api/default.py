from fastapi import APIRouter

default_router = APIRouter()


@default_router.get("/ping", summary="ping")
def ping():
    return "pong"
