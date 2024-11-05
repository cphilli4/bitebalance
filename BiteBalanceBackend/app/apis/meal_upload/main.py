import json
from pathlib import Path


from fastapi import UploadFile

from app.models.domains.meal import NewMeal
from app.models.core import IDModelMixin
from app.db.repositories import MealRepository
from app.utils.s3_bucket_access import upload_meal

from . import crud

# For local test only, Directory to save uploaded images
UPLOAD_DIR = Path("/tmp/uploads/")
UPLOAD_DIR.mkdir(exist_ok=True)


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
    

    
    


