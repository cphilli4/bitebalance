from typing import Any

from fastapi import APIRouter, Depends, Request, status,File, UploadFile, Form

from app.apis.meal_upload import fn_upload_meal
from app.db.dependency import get_repository
from app.models.domains.meal import Meal

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
