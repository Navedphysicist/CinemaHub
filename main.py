from fastapi import FastAPI
from database import Base, engine
from routes import router
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="CinemaHub API",
    description="API for managing movies in CinemaHub",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include movie routes
app.include_router(router)

# Root endpoint


@app.get("/")
def root():
    return {
        "message": "Welcome to CinemaHub API",
        "docs": "/docs",  # Swagger UI endpoint
        "redoc": "/redoc"  # ReDoc endpoint
    }


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
