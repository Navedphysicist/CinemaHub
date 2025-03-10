from sqlalchemy.orm import Session
from models import DbMovie
from schemas import MovieBase
from fastapi import HTTPException, status


def create_movie(db: Session, request: MovieBase):
    # Create new movie instance
    new_movie = DbMovie(
        name=request.name,
        details=request.details,
        image_url=request.image_url
    )

    try:
        # Add and commit to database
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return new_movie
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create movie: {str(e)}"
        )


def get_all_movies(db: Session):
    try:
        # Return all movies
        return db.query(DbMovie).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch movies: {str(e)}"
        )


def get_movie_by_id(db: Session, movie_id: int):
    try:
        # Get single movie by ID
        movie = db.query(DbMovie).filter(DbMovie.id == movie_id).first()
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found"
            )
        return movie
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch movie with ID {movie_id}: {str(e)}"
        )


def update_movie(db: Session, movie_id: int, request: MovieBase):
    try:
        # Get movie to update
        db_movie = db.query(DbMovie).filter(DbMovie.id == movie_id).first()
        if not db_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found"
            )

        # Update movie attributes
        for key, value in request.model_dump().items():
            setattr(db_movie, key, value)

        # Commit changes
        db.commit()
        db.refresh(db_movie)
        return db_movie
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update movie with ID {movie_id}: {str(e)}"
        )


def delete_movie(db: Session, movie_id: int):
    try:
        # Get movie to delete
        movie = db.query(DbMovie).filter(DbMovie.id == movie_id).first()
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found"
            )

        # Delete and commit
        db.delete(movie)
        db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete movie with ID {movie_id}: {str(e)}"
        )
