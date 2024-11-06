from collections import Counter
from datetime import date
import json

from fastapi import UploadFile

from app.models.domains.meal import NewMeal
from app.models.core import IDModelMixin
from app.db.repositories import MealRepository
from app.utils.s3_bucket_access import upload_meal

from . import crud


async def fn_upload_meal(
    meal: UploadFile, 
    label: str,
    meal_repo: MealRepository,
    *,
    raise_duolicate_exception = False,
) -> IDModelMixin:
    
    # analyse meal contents here with chatGPT
    meal_contents = ['avocado', 'brown rice', 'chicken', 'cilantro', 'corn', 'jicama', 'lime', 'tomatoes']
    meal_data = {
        'contents': meal_contents,
        'nutrition_value': 'nutrition_value',
    }
    
    # Save meal on S3 bucket here
    meal_url = await upload_meal(meal)
    
    # Convert Python dictionary to JSON string
    meal_data = json.dumps(meal_data)
    
    new_meal = NewMeal(label=label, url=meal_url, meal_data=meal_data)
    
    return await crud.fn_upload_meal(new_meal, meal_repo)
    

async def fn_get_meal_dates_month(
    meal_repo: MealRepository,
) -> IDModelMixin:
    
    today_month = date.today().month
    
    dates = await crud.fn_get_meal_dates_month(today_month, meal_repo)
    if dates :
        dates_list = [ f"{data.created_at.year}-{data.created_at.month}-{data.created_at.day}"  for data in dates ]
        count_dates = Counter(dates_list)  # Count occurrences of each date
        print("The list of dates is: {}".format(count_dates))
        return count_dates
    return {}

