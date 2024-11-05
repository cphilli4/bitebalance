import json
from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
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

class MealRepository(BaseRepository):
    async def upload_meal(
        self, *, new_meal: Meal
    ) -> MealDBModel:
        query_values = new_meal.model_dump()
        query_values['meal_data'] = json.dumps(query_values['meal_data'])
        print("QUERY VALUE: ", query_values)
        created_meal = await self.db.fetch_one(
            query=NEW_MEAL_SQL, values=query_values
        )
        return MealDBModel(**created_meal)
        
# 
    