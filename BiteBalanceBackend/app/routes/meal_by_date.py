from typing import Any

from fastapi import APIRouter, Depends, Request

from app.apis.meal_dates import fn_get_meal_dates
from app.db.dependency import get_repository

from app.db.repositories import MealRepository


router = APIRouter()


@router.get(
    "/meal-dates/",
    tags=["meal_date"],
    name="meal_date:get",
    )
async def meals_dates(
    request: Request,
    meal_repo: MealRepository= Depends(
        get_repository(MealRepository)
    ),
)->Any:
    
    return await fn_get_meal_dates()
