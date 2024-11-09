from pydantic.types import Json

from app.models.core import IDModelMixin, TimestampsMixin, CoreModel

class Meal(CoreModel):
    label: str
    url: str
    meal_data: Json


class MealDBModel(IDModelMixin, Meal, TimestampsMixin):
    ...


NewMeal = Meal
