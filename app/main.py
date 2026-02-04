"""
Main FastAPI application entry point.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the absolute path to the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Load environment variables FIRST with explicit path
load_dotenv(dotenv_path=env_path)

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
            "test_groq": "/api/test-groq",
        },
    }


@app.get("/api/test-groq")
async def test_groq():
    """Test endpoint to verify Groq API integration."""
    try:
        from app.services.groq_client import get_groq_client
        client = get_groq_client()
        return {
            "status": "success",
            "message": "Groq API client initialized successfully",
            "model": client.model_name,
            "api_key_present": bool(client.api_key)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Groq API client initialization failed: {str(e)}"
        }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "resume-parsing",
    }
