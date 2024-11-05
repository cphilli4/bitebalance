import base64


from openai import OpenAI

from bitebalance.BiteBalanceBackend.app.tests.test_meal.imageAnalyze import ImageRecipeExtractor


def encode_image():
    with open('./Nutrition Table.png', 'rb') as image:
        return base64.b64encode(image.read()).decode('utf-8')



class IngredientRank:
    def __init__(self, ingredients):
        self.ingredients = ''.join(str(x) for x in ingredients)
        self.client = OpenAI()

    def rank_ingredients(self):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": "The following list is in the form 'ingredient|amount in ounces'. "
                                     "Give it a score out of 100 based on the following criteria: "
                                     "Total fruits ≥0.8 cup is maximum 5 points, "
                                     "Whole Fruits ≥0.4 cup is maximum 5 points, "
                                     "Total Vegetables ≥1.1 cup is maximum 5 points, "
                                     "Greens and Beans ≥0.2 cup is maximum 5 points, "
                                     "Whole Grains ≥1.5 oz is maximum 10 points, "
                                     "Dairy ≥1.3 cup is maximum 10 points, "
                                     "Total Protein Foods ≥2.5 oz is maximum 5 points, "
                                     "Seafood and Plant Proteins ≥0.8 oz is maximum 5 points, "
                                     "Refined grains ≤1.8 oz is maximum 10 points, "
                                     "Added sugars ≤6.5% of energy is maximum 10 points, "
                                     "Sodium ≤1.1 gram is maximum 10 points, "
                                     "Saturated Fats ≤8% of energy is maximum 10 points, "
                                     "Fatty Acids (PUFAs + MUFAs)/SFAs ≥2.5 is maximum 10 points. "
                                     "Each ingredient can count in multiple categories. "
                                     "You can give up to the maximum number of points. "
                                     "In essence you want to rank unprocessed foods higher than processed ones. "''
                                     "Format your response as 'X' "
                                     "where X is the sum off all points earned by the ingredients."
                                     "DO NOT respond with any other text"},


                            {"type": "text", "text": self.ingredients}
                        ],
                    }
                ],
                max_tokens=300,
            )
            result = int(completion.choices[0].message.content)
            mod = result % 5
            if mod >2:
                rounded = result + (5-mod)
            else:
                rounded = result - mod
            return rounded
        except Exception as e:
            return "API Error"

extractor = ImageRecipeExtractor('../helpers/meal.JPG')
recipe= extractor.get_recipe()
score = IngredientRank(recipe).rank_ingredients()
extractor1 = ImageRecipeExtractor('../helpers/meal1.JPG')
recipe1= extractor1.get_recipe()
score1 = IngredientRank(recipe1).rank_ingredients()
extractor2 = ImageRecipeExtractor('../helpers/meal2.JPG')
recipe2= extractor2.get_recipe()
score2 = IngredientRank(recipe2).rank_ingredients()
print(recipe)
print(score)
print(recipe1)
print(score1)
print(recipe2)
print(score2)