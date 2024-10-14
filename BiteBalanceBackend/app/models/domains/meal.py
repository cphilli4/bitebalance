from app.models.core import IDModelMixin, TimestampsMixin, CoreModel

class Meal(CoreModel):
    ...


class MealDBModel(Meal, TimestampsMixin):
    ...


NewMeal = Meal
