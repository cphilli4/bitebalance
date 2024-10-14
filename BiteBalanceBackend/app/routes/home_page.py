from typing import Any

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def root()->Any:
    return {"message": "Hello World, welcome to bitebalance"}