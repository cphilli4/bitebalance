# Data schemas for MongoDB
from pydantic import BaseModel

class Image(BaseModel):
  name: str