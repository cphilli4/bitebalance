from pathlib import Path

import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.meals.main import fn_upload_meal
from app.db.repositories import MealRepository

from app.models.domains.meal import NewMeal, MealDBModel
from app.tests.helpers.read_file import read_image

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_upload_meal

# Path to the image on your local machine
# Get the path of the current script (test_script.py)
current_dir = Path(__file__).parent
# current_dir = Path.cwd()
# Construct the path to the 'helpers' folder's image
image_path = current_dir.parent / 'helpers' / 'meal.JPG'



    
@pytest.mark.asyncio
async def test_upload_meal( 
    app: FastAPI, 
    platform_client: AsyncClient, 
    meals_repo: MealRepository,
) -> None:
    meal_label = "my_label"
    meal = read_image(image_path)
    test_results = await FUNCTION_TO_TEST(
        meal,
        meal_label,
        meals_repo,
    )
    test_results_dict = test_results.model_dump()
    
    assert isinstance(test_results, MealDBModel)
    assert test_results_dict["url"] is not None
    assert test_results_dict["meal_data"] is not None
    assert test_results_dict["label"] == meal_label
        

# # Given = Data and any other constants you will be using, When= Is when the API operates on the data given, Then= Where we make assertions. 