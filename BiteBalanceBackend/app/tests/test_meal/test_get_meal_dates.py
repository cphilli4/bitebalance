from collections.abc import Iterable
from datetime import date

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.meals.main import fn_get_meal_dates_month
from app.db.repositories import MealRepository

from app.tests.helpers.upload_meals import upload_meals

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_meal_dates_month


@pytest.mark.asyncio
async def test_get_meal_dates( 
    app: FastAPI, 
    platform_client: AsyncClient, 
    meals_repo: MealRepository,
) -> None:
    meals = ["chicken with salad", "Rice with turkey", "Halal food"]
    _ = await upload_meals(meals, meals_repo)
    test_results = await FUNCTION_TO_TEST(meals_repo)
    
    today = f"{date.today().year}-{date.today().month}-{date.today().day}"
    
    assert isinstance(test_results, Iterable)
    assert today in test_results

        

# Given = Data and any other constants you will be using, When= Is when the API operates on the data given, Then= Where we make assertions. 