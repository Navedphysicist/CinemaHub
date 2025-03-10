from pydantic import BaseModel


# Base schema for Movie data containing common fields
class MovieBase(BaseModel):
    name: str        # Movie title (max 30 chars)
    details: str     # Movie description/plot (max 300 chars)
    image_url: str   # URL to movie poster/cover (max 100 chars)


# Schema for displaying movie data in API responses, includes all base fields plus ID
class MovieDisplay(MovieBase):
    id: int         # Unique identifier for the movie

    class Config:
        from_attributes = True
