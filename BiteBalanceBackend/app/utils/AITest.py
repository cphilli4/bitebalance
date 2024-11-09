import unittest
from bitebalance.BiteBalanceBackend.app.utils.imageAnalyze import ImageRecipeExtractor
from bitebalance.BiteBalanceBackend.app.utils.ingredientAnalyze import IngredientRank


class TestImageRecipeExtractor(unittest.TestCase):

    def test_get_recipe_with_food(self):
        recipe = ImageRecipeExtractor('../tests/test_meal/meal.JPG').get_recipe()
        recipe_check=[i.split('|', 1)[0] for i in recipe]
        expected=['avocado', 'brown rice', 'chicken', 'cilantro', 'corn', 'jicama', 'lime', 'tomato']
        self.assertTrue(set(expected).issubset(recipe_check))
        score = IngredientRank(recipe).rank_ingredients()
        self.assertTrue(70>=score>=60)

    def test_get_recipe_no_food_detected(self):
        extractor = ImageRecipeExtractor('../tests/test_meal/not_food.JPG')
        recipe = extractor.get_recipe()
        self.assertEqual(recipe, ["No food detected."])

    def test_get_recipe_api_error(self):
        extractor = ImageRecipeExtractor('../tests/test_meal/not_image.TXT')
        recipe= extractor.get_recipe()
        self.assertEqual(recipe, "API Error")