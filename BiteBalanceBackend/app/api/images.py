from fastapi import APIRouter, HTTPException
from db.session import db
from schemas.images import Image

router = APIRouter()

@router.get("/images/hello")
async def hello_world():
  return {"message": "Hello World!"}