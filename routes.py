from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import MovieBase, MovieDisplay
import db_movie

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

# Create a new movie


@router.post("/", response_model=MovieDisplay, status_code=status.HTTP_201_CREATED)
def create_movie(request: MovieBase, db: Session = Depends(get_db)):
    return db_movie.create_movie(db, request)

# Get all movies


@router.get("/", response_model=List[MovieDisplay])
def get_all_movies(db: Session = Depends(get_db)):
    return db_movie.get_all_movies(db)

# Get a specific movie by ID


@router.get("/{movie_id}", response_model=MovieDisplay)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    return db_movie.get_movie_by_id(db, movie_id)

# Update a movie


@router.put("/{movie_id}", response_model=MovieDisplay)
def update_movie(movie_id: int, request: MovieBase, db: Session = Depends(get_db)):
    return db_movie.update_movie(db, movie_id, request)

# Delete a movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie.delete_movie(db, movie_id)
    return None
