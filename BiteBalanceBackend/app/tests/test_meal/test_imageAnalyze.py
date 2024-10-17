import unittest
from bitebalance.BiteBalanceBackend.app.tests.test_meal.imageAnalyze import ImageRecipeExtractor


class TestImageRecipeExtractor(unittest.TestCase):

    def test_get_recipe_with_food(self):
        extractor = ImageRecipeExtractor('https://www.kitchensanctuary.com/wp-content/uploads/2019/09/Spaghetti-Bolognese-square-FS-0204.jpg')
        recipe= extractor.get_recipe()
        self.assertEqual(recipe,['garlic', 'green onions', 'ground meat', 'olive oil', 'onion', 'parmesan cheese', 'pepper', 'salt', 'spaghetti', 'tomato sauce'])

    def test_get_recipe_no_food_detected(self):
        extractor = ImageRecipeExtractor('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmWbawbNF-2wzBvaljDWDvsilTM79knAD9Zw&s')
        recipe = extractor.get_recipe()
        self.assertEqual(recipe, ["No food detected."])

    def test_get_recipe_api_error(self):
        extractor = ImageRecipeExtractor('https://my.stevens.edu/')
        recipe= extractor.get_recipe()
        self.assertEqual(recipe, "API Error")