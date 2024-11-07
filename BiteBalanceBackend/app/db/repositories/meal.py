import json
from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import CreatedAtMixin
from app.models.domains.meal import (
    Meal,
    MealDBModel
)

NEW_MEAL_SQL = """
    INSERT INTO meals(label, url, meal_data)
    VALUES(:label, :url,  :meal_data)
    RETURNING *;
"""

GET_MEAL_SQL = """
    SELECT url, label, meal_data;
"""

GET_MEAL_DATES_FOR_MONTH_SQL = """
    SELECT created_at FROM meals WHERE EXTRACT(MONTH FROM created_at) =:month;
"""

class MealRepository(BaseRepository):
    async def upload_meal(
        self, *, new_meal: Meal
    ) -> MealDBModel:
        query_values = new_meal.model_dump()
        query_values['meal_data'] = json.dumps(query_values['meal_data'])
        created_meal = await self.db.fetch_one(
            query=NEW_MEAL_SQL, values=query_values
        )
        return MealDBModel(**created_meal)
    
    async def get_meal_dates_month(self, *, month: int):
        query_value = {'month': month}
        
        created_meals = await self.db.fetch_all(
            query=GET_MEAL_DATES_FOR_MONTH_SQL, values=query_value
        )
        
        if created_meals: 
            created_meal_dates = [CreatedAtMixin(**created_meal) for created_meal in created_meals]
            return  created_meal_dates
        return None
        
    