from fastapi import APIRouter

ping_router = APIRouter()


@ping_router.get("/ping")
def ping():
    return "pong"
