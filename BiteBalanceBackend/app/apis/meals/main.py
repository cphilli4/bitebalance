from collections import Counter
from datetime import date, timedelta, datetime
import json
from typing import List, Dict, Optional

from fastapi import UploadFile

from app.models.domains.meal import NewMeal, MealDBModel

from app.models.core import IDModelMixin, CreatedAtMixin
from app.db.repositories import MealRepository

from app.utils.s3_bucket_access import upload_meal, pre_signed_image_url
from app.utils.imageAnalyze import ImageRecipeExtractor
from app.utils.ingredientAnalyze import IngredientRank

from app.models.exceptions.crud_exception import BadRequestException

from . import crud


async def fn_upload_meal(
    meal: UploadFile, 
    label: str,
    meal_repo: MealRepository,
    *,
    raise_duolicate_exception = False,
) -> IDModelMixin:
    
    # analyse meal contents here with chatGPT
    filename = meal.filename
    meal_image = await meal.read()
    recipe_extractor = ImageRecipeExtractor(meal_image)
    recipe = recipe_extractor.get_recipe()
    # form of "ingredient|amount in oz"
    score = IngredientRank(recipe).rank_ingredients()
    meal_data = {
        'contents': recipe,
        'nutrition_value': score
    }
    
    # Save meal on S3 bucket here
    meal_url = await upload_meal(meal_image, filename)
    
    # Convert Python dictionary to JSON string
    meal_data = json.dumps(meal_data)
    
    new_meal = NewMeal(label=label, url=meal_url, meal_data=meal_data)
    
    meal_db_data = await crud.fn_upload_meal(new_meal, meal_repo)
    meal_db_data = meal_db_data.model_dump()
    meal_db_data['url'] = await pre_signed_image_url(meal_url)
    
    return meal_db_data
    

async def fn_get_meal_dates_month(
    date: str,
    meal_repo: MealRepository,
) -> IDModelMixin:
    
    try:
        month = datetime.strptime(date, "%m-%d-%Y").month
    except Exception:
        raise BadRequestException(message="Date format not supported")
    
    dates = await crud.fn_get_meal_dates_month(month, meal_repo)
    if dates :
        dates_list = [ f"{data.created_at.year}-{data.created_at.month}-{data.created_at.day}"  for data in dates ]
        count_dates = Counter(dates_list)  # Count occurrences of each date
        return count_dates
    return {}


async def fn_get_meal_day(day: str, meal_repo: MealRepository)->Optional[List[MealDBModel]]:
    try:
        day = date.fromisoformat(day)
        meals = await crud.fn_get_meal_day(day, meal_repo)
    except Exception:
        raise BadRequestException(message="Date format not supported")
    if meals:
        for index in range(len(meals)):
            meals[index].url =  await pre_signed_image_url(meals[index].url)
        return meals
    return []
    


async def fn_get_meal_start_end_date(start: str, end: str , meal_repo: MealRepository)->Optional[Dict[date, int]]:
    try:
        start = date.fromisoformat(start)
        end = date.fromisoformat(end) + timedelta(days=1)
    except Exception:
        raise BadRequestException(message="Date format not supported")
    
    return await crud.fn_get_meal_start_end_date(start, end, meal_repo)
    