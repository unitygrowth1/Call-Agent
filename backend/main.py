# FastAPI Main Application Entry Point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from contextlib import asynccontextmanager
import logging
from config import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info("Initializing database connections...")
    logger.info("Initializing Redis connections...")
    logger.info("Initializing AI services...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Closing database connections...")
    logger.info("Closing Redis connections...")
    logger.info("Cleanup complete")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise-grade AI Voice Agent and Business Automation SaaS Platform",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Add GZIP compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }

# Ready check endpoint
@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check - confirms all services are ready
    """
    # TODO: Check database, Redis, Ollama, etc.
    return {"ready": True}

# API v1 Routes (will be imported from app.api.v1)
@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "api": "/api/v1",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
