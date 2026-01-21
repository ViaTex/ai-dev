"""
Main FastAPI application entry point.
"""

from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.resume import router as resume_router

# Create FastAPI app
app = FastAPI(
    title="Resume Parsing API",
    description="LLM-based resume parsing service using Groq API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Resume Parsing API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "parse_resume": "/api/parse-resume",
            "health": "/api/health",
        },
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "resume-parsing",
    }
