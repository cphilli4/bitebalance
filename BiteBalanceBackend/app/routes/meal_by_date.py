from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends, Request, status,File, UploadFile, Form

from app.apis.meal_upload import fn_upload_meal
from app.db.dependency import get_repository
from app.models.domains.meal import Meal

from app.db.repositories import MealRepository


router = APIRouter()


@router.get(
    "/meal-dates/",
    tags=["meal_date"],
    name="meal_date:get",
    )
async def meals_date(
    request: Request,
    date: datetime, 
  
)->Any:
    ...
