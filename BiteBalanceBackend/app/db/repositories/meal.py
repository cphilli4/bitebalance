from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
from app.models.domains.meal import (
    Meal,
    MealDBModel
)

NEW_MEAL_SQL = """
    INSERT INTO meals(url, label)
    VALUES(:url, :label)
    RETURNING *;
"""

GET_MEAL_SQL = """
    SELECT url, label;
"""

class MealRepository(BaseRepository):
    async def upload_meal(
        self, *, new_meal: Meal
    ) -> MealDBModel:
        query_values = new_meal.model_dump()
        
        created_meal = await self.db.fetch_one(
            query=NEW_MEAL_SQL, values=query_values
        )
        return MealDBModel(**created_meal)
    

    