
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import BigInteger


class CityInfo(BaseModel):
    provience: str
    country: str
    country_population: int

class CityCreateSchema(CityInfo):
    pass
