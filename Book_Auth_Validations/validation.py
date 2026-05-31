from typing import Optional
from pydantic import BaseModel,Field, StrictBool

class Book_Request(BaseModel):
    # id : Optional[int] = None
    id:Optional[int]=Field(default = None,description="In creating a post req id is optional and not required")
    name :str = Field(min_length=3,max_length=35)
    description:str =Field(min_length=3,max_length=200)
    rating:float=Field(gt=-1,lt=6)
    is_read:bool=Field(description="Values of True and False are accepted only")
    published_date:int=Field(gt=1000,lt=2027)

    model_config = {
        "json_schema_extra" :{
            "example":{
                "id" : 1,
                "name":"Around the world in eighty days",
                "description":"A journey of the whole world ,a lot of fun",
                "rating":5,
                "is_read":False,
                "published_date":2012
            }
        }
    }
# Allows only T and F -> StrictBool