from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RecipeSourceType(Enum):
    bar = "bar"
    book = "book"
    youtube_video = "youtube_video"


class UnitType(Enum):
    weight = "weight"
    volume = "volume"


class Ingredients(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    abv_in_percent = Column(Integer, nullable=True)
    brix_in_percent = Column(Integer, nullable=True)
    description = Column(String, nullable=True)

    recipes = relationship("RecipeIngredients", back_populates="ingredient")


class Youtubers(Base):
    __tablename__ = "youtubers"
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, nullable=False)
    full_name = Column(String, nullable=False)
    channel_name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class YouTubeVideos(Base):
    __tablename__ = "youtube_videos"
    source_id = Column(Integer, ForeignKey("sources.id"), primary_key=True)
    youtuber_id = Column(Integer, ForeignKey("youtubers.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    source = relationship("Sources", back_populates="youtube_video")
    youtuber = relationship("Youtubers")


class Cocktails(Base):
    __tablename__ = "cocktails"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Sources(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(RecipeSourceType), nullable=False)
    name = Column(String, nullable=False)

    youtube_video = relationship(
        "YouTubeVideos", back_populates="source", uselist=False
    )
    bar = relationship("Bars", back_populates="source", uselist=False)
    book = relationship("Books", back_populates="source", uselist=False)


class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    cocktail_id = Column(Integer, ForeignKey("cocktails.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    abv_in_percent = Column(Integer, nullable=True)
    method = Column(String, nullable=True)

    cocktail = relationship("Cocktails")
    recipes = relationship("Recipes", back_populates="source")
    ingredients = relationship("RecipeIngredients", back_populates="recipe")


class MeasuringUnits(Base):
    __tablename__ = "measuring_units"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    num_mls_or_gs = Column(Float, nullable=False)


class RecipeIngredients(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float, nullable=False)
    unit_id = Column(Integer, ForeignKey("measuring_units.id"), nullable=False)

    recipe = relationship("Recipes", back_populates="ingredients")
    ingredient = relationship("Ingredients", back_populates="recipes")
    unit = relationship("MeasuringUnits")


class Bartenders(Base):
    __tablename__ = "bartenders"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey("bartending_schools.id"), nullable=True)

    school = relationship("BartendingSchools")
    recipes = relationship("Recipes", back_populates="bartender")


class BartendingSchools(Base):
    __tablename__ = "bartending_schools"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    bartenders = relationship("Bartenders", back_populates="school")
    bars = relationship("Bars", back_populates="school")


class Bars(Base):
    __tablename__ = "bars"
    source_id = Column(Integer, ForeignKey("sources.id"), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    school_id = Column(Integer, ForeignKey("bartending_schools.id"), nullable=True)

    source = relationship("Sources", back_populates="bar")
    city = relationship("Cities")
    school = relationship("BartendingSchools")


class Countries(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class States(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    country = relationship("Countries")


class Cities(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)

    state = relationship("States")


class Books(Base):
    __tablename__ = "books"
    source_id = Column(Integer, ForeignKey("sources.id"), primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_published = Column(Integer, nullable=False)

    source = relationship("Sources", back_populates="book")
