import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get environment
ENV = os.getenv("ENV", "development")

# Database URLs
if ENV == "production":
    # Use in-memory SQLite in production (Vercel)
    DATABASE_URL = "sqlite:///:memory:"
else:
    # Use file-based SQLite in development
    DATABASE_URL = "sqlite:///./cinemaHub.db"

# Create engine with appropriate settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    # Enable SQLite foreign key support
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create tables and add initial data for in-memory database


def init_db():
    if ENV == "production":
        # Create all tables in memory
        Base.metadata.create_all(bind=engine)


def get_db():
    if ENV == "production":
        # Initialize in-memory database for each request
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enable foreign key support for SQLite


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
