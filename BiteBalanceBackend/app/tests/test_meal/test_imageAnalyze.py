import unittest
from bitebalance.BiteBalanceBackend.app.tests.test_meal.imageAnalyze import ImageRecipeExtractor


class TestImageRecipeExtractor(unittest.TestCase):

    def test_get_recipe_with_food(self):
        extractor = ImageRecipeExtractor('../helpers/meal.JPG')
        recipe= extractor.get_recipe()
        expected=['avocado', 'brown rice', 'chicken', 'cilantro', 'corn', 'jicama', 'lime', 'tomatoes']
        self.assertEqual(recipe, expected)

    def test_get_recipe_no_food_detected(self):
        extractor = ImageRecipeExtractor('../helpers/not_food.JPG')
        recipe = extractor.get_recipe()
        self.assertEqual(recipe, ["No food detected."])

    def test_get_recipe_api_error(self):
        extractor = ImageRecipeExtractor('../helpers/not_image.TXT')
        recipe= extractor.get_recipe()
        self.assertEqual(recipe, "API Error")