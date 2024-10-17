from openai import OpenAI

class ImageRecipeExtractor:
    def __init__(self, image_url):
        self.image_url = image_url
        self.client = OpenAI()

    def get_recipe(self):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What is the recipe of the food in the image? If no food is present, please respond with 'No food detected'. Otherwise, just respond with a comma-separated ingredient list with no measurements."},
                            {"type": "image_url", "image_url": {"url": self.image_url}},
                        ],
                    }
                ],
                max_tokens=300,
            )
            return sorted(completion.choices[0].message.content.split(", "))
        except Exception as e:
            return "API Error"



