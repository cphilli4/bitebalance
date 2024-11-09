# import base64

# from openai import OpenAI

# class ImageRecipeExtractor:
#     def __init__(self, image_path):
#         self.image_path = image_path
#         self.client = OpenAI()

#     def encode_image(self):
#         with open(self.image_path, 'rb') as image:
#             return base64.b64encode(image.read()).decode('utf-8')

#     def get_recipe(self):
#         encoded_image = self.encode_image()
#         try:
#             completion = self.client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": [
#                             {"type": "text", "text": "What is the recipe of the food in the image? If no food is present, please respond with 'No food detected'. Otherwise, just respond with a comma-separated ingredient list with no measurements."},
#                             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.encode_image()}"}},
#                         ],
#                     }
#                 ],
#                 max_tokens=300,
#             )
#             return sorted(completion.choices[0].message.content.split(", "))
#         except Exception as e:
#             return "API Error"
