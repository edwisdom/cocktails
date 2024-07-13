from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class RecipeSourceType(str, Enum):
    bar = "bar"
    book = "book"
    youtube_video = "youtube_video"


class UnitType(str, Enum):
    weight = "weight"
    volume = "volume"


class Ingredients(BaseModel):
    id: int
    name: str
    abv_in_percent: Optional[int] = None
    brix_in_percent: Optional[int] = None
    description: Optional[str] = None


class Youtubers(BaseModel):
    id: int
    channel_id: int
    full_name: str
    channel_name: str
    description: Optional[str] = None


class YouTubeVideos(BaseModel):
    source_id: int
    youtuber_id: int
    name: str
    description: Optional[str] = None


class Cocktails(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class Sources(BaseModel):
    id: int
    type: RecipeSourceType
    name: str


class Recipes(BaseModel):
    id: int
    cocktail_id: int
    source_id: int
    abv_in_percent: Optional[int] = None
    method: Optional[str] = None


class MeasuringUnits(BaseModel):
    id: int
    name: str
    unit_type: UnitType
    num_mls_or_gs: float


class RecipeIngredients(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: float
    unit_id: int


class Bartenders(BaseModel):
    id: int
    name: str
    school_id: Optional[int]


class BartendingSchools(BaseModel):
    id: int
    name: str
    description: Optional[str]


class Bars(BaseModel):
    source_id: int
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    city_id: Optional[int] = None
    school_id: Optional[int] = None


class Countries(BaseModel):
    id: int
    name: str


class States(BaseModel):
    id: int
    name: str
    country_id: int


class Cities(BaseModel):
    id: int
    name: str
    state_id: int


class Books(BaseModel):
    source_id: int
    title: str
    author: str
    year_published: int
