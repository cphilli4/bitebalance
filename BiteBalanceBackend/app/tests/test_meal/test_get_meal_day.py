from collections.abc import Iterable
from datetime import date, timedelta

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.meals.main import fn_get_meal_day
from app.models.domains.meal import MealDBModel
from app.db.repositories import MealRepository

from app.tests.helpers.upload_meals import upload_meals

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_meal_day


@pytest.mark.asyncio
async def test_get_meal_day( 
    app: FastAPI, 
    platform_client: AsyncClient, 
    meals_repo: MealRepository,
) -> None:
    meals = ["chicken with salad"]
    _ = await upload_meals(meals, meals_repo) 
    
    today = date.today()
    today = f"{today.year}-{today.month}-{today.day}" if len(str(today.day)) > 1 else f"{today.year}-{today.month}-0{today.day}"
    
    test_results = await FUNCTION_TO_TEST(today, meals_repo)
    
    meal_labels =  [ test_result.label for test_result in test_results]
    
    assert isinstance(test_results, Iterable)
    assert isinstance(test_results[0], MealDBModel)
    assert meals[0] in meal_labels

        

# # Given = Data and any other constants you will be using, When= Is when the API operates on the data given, Then= Where we make assertions. 