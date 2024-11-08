from collections.abc import Iterable
from datetime import date, timedelta

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.meals.main import fn_get_meal_start_end_date
from app.db.repositories import MealRepository

from app.tests.helpers.upload_meals import upload_meals

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_meal_start_end_date


@pytest.mark.asyncio
async def test_get_meal_start_end_date( 
    app: FastAPI, 
    platform_client: AsyncClient, 
    meals_repo: MealRepository,
) -> None:
    meals = ["chicken with salad"]
    _ = await upload_meals(meals, meals_repo) 
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    today = f"{today.year}-{today.month}-{today.day}" if len(str(today.day)) > 1 else f"{today.year}-{today.month}-0{today.day}"
    yesterday = f"{yesterday.year}-{yesterday.month}-{yesterday.day}" if len(str(yesterday.day)) > 1 else f"{yesterday.year}-{yesterday.month}-0{yesterday.day}"
    
    test_results = await FUNCTION_TO_TEST(yesterday, today, meals_repo)
    
    datetime_list =  [ test_result.created_at for test_result in test_results]
    
    date_list = [ f"{date.year}-{date.month}-{date.day}" for date in datetime_list]
    
    today = date.today()
    today = f"{today.year}-{today.month}-{today.day}" 
    
    assert isinstance(test_results, Iterable)
    assert today in date_list

        

# # Given = Data and any other constants you will be using, When= Is when the API operates on the data given, Then= Where we make assertions. 