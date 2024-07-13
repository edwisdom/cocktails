from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class RecipeSourceType(str, Enum):
    bar = "bar"
    book = "book"
    youtube_video = "youtube_video"


class Ingredients(BaseModel):
    id: int
    name: str
    abv_in_percent: int
    brix_in_percent: int
    description: str


class Youtubers(BaseModel):
    id: int
    channel_id: int
    full_name: str
    channel_name: str
    description: str


class YouTubeVideos(BaseModel):
    source_id: int
    youtuber_id: int
    name: str
    description: str


class Cocktails(BaseModel):
    id: int
    name: str
    description: str


class Sources(BaseModel):
    id: int
    type: RecipeSourceType
    name: str


class Recipes(BaseModel):
    id: int
    cocktail_id: int
    source_id: int
    abv_in_percent: int
    method: str


class MeasuringUnits(BaseModel):
    id: int
    name: str
    num_mls: float


class RecipeIngredients(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: float
    unit_id: int


class Bartenders(BaseModel):
    id: int
    name: str
    school_id: int


class BartendingSchools(BaseModel):
    id: int
    name: str
    description: str


class Bars(BaseModel):
    source_id: int
    name: str
    description: str
    address: str
    city_id: int
    school_id: int


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
