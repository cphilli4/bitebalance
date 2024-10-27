import base64
import math

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
            completion1 = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": "The following list is in the form 'ingredient|amount in ounces'. Give it a score out of 100 based on the table given. Each ingredient can count in multiple categories. Only respond in with the total score number, no other text"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image()}"}},
                            {"type": "text", "text": self.ingredients}
                        ],
                    }
                ],
                max_tokens=300,
            )
            completion2 = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": "The following list is in the form 'ingredient|amount in ounces'. Give it a score out of 100 based on the table given. Each ingredient can count in multiple categories. Only respond in with the total score number, no other text"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image()}"}},
                            {"type": "text", "text": self.ingredients}
                        ],
                    }
                ],
                max_tokens=300,
            )
            completion3 = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": "The following list is in the form 'ingredient|amount in ounces'. Give it a score out of 100 based on the table given. Each ingredient can count in multiple categories. Only respond in with the total score number, no other text"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image()}"}},
                            {"type": "text", "text": self.ingredients}
                        ],
                    }
                ],
                max_tokens=300,
            )

            return math.floor((int(completion1.choices[0].message.content)+int(completion2.choices[0].message.content)+int(completion3.choices[0].message.content))/3)
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