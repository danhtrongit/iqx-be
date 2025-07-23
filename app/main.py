from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.database import setup_timescale
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_db_client():
    """Initialize database connections when the application starts."""
    logger.info("Connecting to PostgreSQL/TimescaleDB...")
    try:
        # Set up TimescaleDB extension if enabled
        setup_timescale()
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connections when the application shuts down."""
    logger.info("Closing database connections...")


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "IQX API is running. Go to /docs for the API documentation."}

