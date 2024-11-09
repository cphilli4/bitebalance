from typing import List, Optional
from datetime import date

from app.models.core import IDModelMixin
from app.models.domains.meal import NewMeal, MealDBModel
from app.db.repositories import MealRepository


async def fn_upload_meal(
    new_meal: NewMeal,
    meal_repo: MealRepository,
) -> IDModelMixin:
    return await meal_repo.upload_meal(
        new_meal=new_meal,
    )
    
    
async def fn_get_meal_dates_month(
    month: int,
    meal_repo: MealRepository,
) -> IDModelMixin:
    return await meal_repo.get_meal_dates_month(month=month)


async def fn_get_meal_day(day: date, meal_repo: MealRepository)->List[MealDBModel]:
    return await meal_repo.get_meal_day(day=day)

async def fn_get_meal_start_end_date(start: date, end: date , meal_repo: MealRepository)->Optional[List[date]]:
    return await meal_repo.get_meal_start_end_date(start=start, end=end)