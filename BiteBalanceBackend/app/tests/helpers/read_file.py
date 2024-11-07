from pathlib import Path
import io
from fastapi import UploadFile



# For local test only, Directory to save uploaded images
IMAGE_PATH = Path(__file__).parent /'meal.JPG'


# Function to read the image
def read_image(image_path):
    
    try:
        # Read the image as binary
        with open(image_path, "rb") as f:
            file_bytes = f.read()
        
        # Simulate UploadFile object using an in-memory stream (io.BytesIO)
        file_object = UploadFile(filename=image_path.name, file=io.BytesIO(file_bytes))
        
        return  file_object
    except FileNotFoundError:
        raise FileNotFoundError("Image not found at the specified path.")
    

