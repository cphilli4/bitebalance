import json

from app.db.repositories import MealRepository
from app.models.domains.meal import NewMeal


async def upload_meals(
    meals: list,
    meal_repo: MealRepository,
) -> None:
    
    for meal in meals:
        label = meal
        # analyse meal contents here with chatGPT
        meal_contents = ['avocado', 'brown rice', 'chicken', 'cilantro', 'corn', 'jicama', 'lime', 'tomatoes']
        meal_data = {
            'contents': meal_contents,
            'nutrition_value': 'nutrition_value',
        }
        
        # Save meal on S3 bucket here
        meal_url = "https://s3.amazonaws.com/"
        
        # Convert Python dictionary to JSON string
        meal_data = json.dumps(meal_data)
        
        new_meal = NewMeal(label=label, url=meal_url, meal_data=meal_data)
        
        await meal_repo.upload_meal(
            new_meal=new_meal,
        )
    