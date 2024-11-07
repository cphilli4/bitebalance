from typing import Any, Optional

from fastapi import APIRouter, Depends, Request,File, UploadFile, Form, Query

from app.apis.meals import (
    fn_upload_meal,
   fn_get_meal_dates_month,
)
from app.db.dependency import get_repository

from app.db.repositories import MealRepository


router = APIRouter()


@router.post(
    "/upload-meal-with-label",
    tags=["meal_label"],
    name="meal_label:post",
    )
async def upload_meal_with_label(
    request: Request,
    meal: UploadFile = File(...), 
    label: str = Form(...),
    meal_repo: MealRepository= Depends(
        get_repository(MealRepository)
    ),
)->Any:
    if label is None:
        label = ''
    return await fn_upload_meal(meal, label, meal_repo)


@router.get(
    "/meal-dates",
    tags=["meal_date"],
    name="meal_date:get",
    )
async def meals_dates(
    request: Request,
    date: Optional[str] = Query(None, description="Date string in format 'MM-DD-YYYY'"),
    meal_repo: MealRepository= Depends(
        get_repository(MealRepository)
    ),
)->Any:
    
    return await fn_get_meal_dates_month(date, meal_repo)