import base64
import json
import os
import re

from bitebalance.BiteBalanceBackend.app.utils.imageAnalyze import ImageRecipeExtractor
from bitebalance.BiteBalanceBackend.app.utils.ingredientAnalyze import IngredientRank


def encode_image(image_path):
    with open(image_path, 'rb') as image:
        encoded = base64.b64encode(image.read()).decode('utf-8')
        sanitized = re.sub(r'[^a-zA-Z0-9]', '_', encoded)
        return sanitized[:100]

def create_recipe_json(image_path: str) -> None:
    output_json_path = './jsons/' +encode_image(image_path) + '.json'

    if os.path.exists(output_json_path):
        print("File already exists. Skipping creation.")
        return

    recipe_extractor = ImageRecipeExtractor(image_path)
    recipe = recipe_extractor.get_recipe()

    ingredients_info = []
    for ingredient in recipe:
        ingredient_name, amount = ingredient.split('|', 1)
        ingredients_info.append({
            'ingredient': ingredient_name.strip(),
            'amount': amount.strip()
        })

    score = IngredientRank(recipe).rank_ingredients()

    recipe_data = {
        'ingredients': ingredients_info,
        'score': score
    }

    with open(output_json_path, 'w') as json_file:
        json.dump(recipe_data, json_file, indent=4)
    print(f'Recipe JSON has been saved to {output_json_path}')

if __name__ == "__main__":
    create_recipe_json('../tests/test_meal/meal.JPG')