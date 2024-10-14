from pathlib import Path

from fastapi import UploadFile, HTTPException

from app.models.domains.meal import NewMeal
from app.models.core import IDModelMixin
from app.db.repositories import MealRepository

from . import crud

# For local test only, Directory to save uploaded images
UPLOAD_DIR = Path("/tmp/uploads/")
UPLOAD_DIR.mkdir(exist_ok=True)

async def fn_create_meal(
    meal: UploadFile, 
    label: str,
    meal_repo: MealRepository,
    *,
    raise_duolicate_exception = False,
) -> IDModelMixin:
    # process meal image here
    
    # new_meal = NewMeal()
    
    # return await crud.fn_create_meal()
    
    # For Local test onlt, save the uploaded image file
    image_path = UPLOAD_DIR / meal.filename
    
    try:
        # Save the file to the uploads directory
        with image_path.open("wb") as buffer:
            buffer.write(await meal.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload failed")
    
    return {"filename": meal.filename, "file_path": str(image_path), "label": str(label)}
    
    


