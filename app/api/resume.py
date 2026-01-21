"""
API endpoints for resume parsing.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.resume_schema import ParsedResumeResponse
from app.utils.file_parser import parse_resume_file
from app.services.groq_client import groq_client

router = APIRouter(prefix="/api", tags=["resume"])


@router.post("/parse-resume", response_model=ParsedResumeResponse)
async def parse_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)")
):
    """
    Upload and parse a resume file.
    
    This endpoint:
    1. Accepts a PDF or DOCX resume file
    2. Extracts text from the file
    3. Sends the text to Groq LLM for structured parsing
    4. Returns parsed resume data as JSON
    
    Args:
        file: Uploaded resume file
        
    Returns:
        ParsedResumeResponse with structured resume data
        
    Raises:
        HTTPException: If file processing or parsing fails
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided"
        )
    
    if not (file.filename.lower().endswith('.pdf') or 
            file.filename.lower().endswith('.docx')):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )
    
    try:
        # Step 1: Extract text from uploaded file
        resume_text = await parse_resume_file(file)
        
        # Step 2: Send to Groq API for parsing
        parsed_data = await groq_client.parse_resume(resume_text)
        
        # Step 3: Return structured response
        return ParsedResumeResponse(
            success=True,
            message="Resume parsed successfully",
            data=parsed_data
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions from parsing functions
        raise
    
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during resume parsing: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Simple status message
    """
    return {"status": "healthy", "service": "resume-parsing-api"}
