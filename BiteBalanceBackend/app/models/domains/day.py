from pydantic import BaseModel, constr

class Day(BaseModel):
    date_str: constr(regex=r'^\d{4}-\d{2}-\d{2}$') # type: ignore

