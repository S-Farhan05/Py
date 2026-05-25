from typing import Optional
from pydantic import BaseModel,Field, StrictBool

class Book_Request(BaseModel):
    id : Optional[int] = None
    name :str = Field(min_length=3,max_length=15)
    description:str =Field(min_length=3,max_length=200)
    rating:int=Field(gt=-1,lt=6)
    is_read:bool=Field(description="Values of True and False are accepted only")


# Allows only T and F -> StrictBool