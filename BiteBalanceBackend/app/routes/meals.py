from datetime import date
from typing import Any, List, Dict, Optional

from fastapi import APIRouter, Depends, Request,File, UploadFile, Form, Query

from app.models.domains.meal import MealDBModel
from app.models.core import CreatedAtMixin
from app.apis.meals import (
    fn_upload_meal,
    fn_get_meal_dates_month,
    fn_get_meal_day,
    fn_get_meal_start_end_date,
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

@router.get(
    "/day-meals",
    tags=["meals_day"],
    name="meals_day:get",
    )
async def meals_day(
    request: Request,
    day:str = Query(..., description="Date in yyyy-mm-dd format", regex=r'^\d{4}-\d{2}-\d{2}$'),
    meal_repo: MealRepository= Depends(
        get_repository(MealRepository)
    ),
)->Optional[List[MealDBModel]]:
    
    return await fn_get_meal_day(day, meal_repo)


@router.get(
    "/month-meals",
    tags=["meals_month"],
    name="meals_month:get",
    )
async def meals_date_start_end(
    request: Request,
    start_date:str = Query(..., description="Date in yyyy-mm-dd format", regex=r'^\d{4}-\d{2}-\d{2}$'),
    end_date:str = Query(..., description="Date in yyyy-mm-dd format", regex=r'^\d{4}-\d{2}-\d{2}$'),
    meal_repo: MealRepository= Depends(
        get_repository(MealRepository)
    ),
)->Optional[Dict[date, int]]:
    
    return await fn_get_meal_start_end_date(start_date, end_date, meal_repo)
