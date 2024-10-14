from app.models.core import IDModelMixin
from app.models.domains.meal import NewMeal, Meal

from app.db.repositories import MealRepository


async def fn_upload_meal(
    new_meal: NewMeal,
    meal_repo: MealRepository,
) -> IDModelMixin:
    return await meal_repo.upload_meal(
        new_meal=new_meal,
    )