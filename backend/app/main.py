"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI app"""
    # Startup
    print("Starting Job Discovery Platform API")
    yield
    # Shutdown
    print("Shutting down Job Discovery Platform API")


# Initialize FastAPI app
app = FastAPI(
    title="Job Discovery Platform API",
    description="AI-powered job discovery platform with web scraping and NLP analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "Job Discovery Platform API is running",
        "data": {"version": "1.0.0", "status": "healthy"}
    }


# Basic job search endpoint (placeholder)
@app.post("/api/jobs/search/hashtags")
async def search_jobs_by_hashtags(request: dict):
    """Simple hashtag-based job search"""
    return {
        "success": True,
        "message": "Search functionality not yet implemented",
        "data": {
            "hashtags": request.get("hashtags", []),
            "jobs": [],
            "total_count": 0
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
