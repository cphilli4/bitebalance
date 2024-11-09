import json
from datetime import date
from typing import List

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
    SELECT created_at 
    FROM meals 
    WHERE EXTRACT(MONTH FROM created_at) =:month;
"""

GET_MEAL_FOR_DAY_SQL = """
    SELECT * 
    FROM meals 
    WHERE created_at::date =:day;
"""

GET_MEAL_START_END_DATE ="""
    SELECT DATE(created_at) AS date, COUNT(*) AS count 
    FROM meals 
    WHERE created_at >=:start AND created_at <:end
    GROUP BY DATE(created_at);
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
            print('in here we created a meal date', created_meal_dates)
            return  created_meal_dates
        return None
        
    async def get_meal_day(self, *, day: date):
        query_value = {'day': day}
        
        meals = await self.db.fetch_all(
            query=GET_MEAL_FOR_DAY_SQL, values=query_value
        )
        
        if meals: 
            day_meal = [MealDBModel(**meal) for meal in meals]
            return  day_meal
        return None

    async def get_meal_start_end_date(self, *, start: date, end: date):
        query_value = {'start': start, 'end': end}
        created_meals = await self.db.fetch_all(
            query=GET_MEAL_START_END_DATE, values=query_value
        )
        print('meals', created_meals)
        if created_meals: 
            created_meal_dates = {created_meal["date"]: created_meal["count"] for created_meal in created_meals}
            print('created meals dates', created_meal_dates)
            return  created_meal_dates
        return None