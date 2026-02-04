"""
API endpoints for resume parsing.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import ValidationError

from app.schemas.resume_schema import ParsedResumeResponse, ResumeData
from app.utils.file_parser import parse_resume_file
from app.services.groq_client import get_groq_client

router = APIRouter(prefix="/api", tags=["resume"])


def _transform_parsed_data(data: dict) -> dict:
    """
    Corrects the structure and types of parsed resume data to match Pydantic models.
    """
    # Fix social links: Replace non-URL placeholders with None
    social_links = data.get("personal_information", {}).get("social_links")
    if social_links:
        for key, value in social_links.items():
            if not isinstance(value, str) or not value.startswith(('http://', 'https://')):
                social_links[key] = None

    # Fix awards: Convert list of dicts to list of strings
    additional_info = data.get("additional_information", {})
    if additional_info and "awards" in additional_info:
        awards_list = additional_info.get("awards", [])
        if awards_list and isinstance(awards_list[0], dict):
            corrected_awards = [
                item.get("award_name", "") for item in awards_list if "award_name" in item
            ]
            additional_info["awards"] = corrected_awards
            
    return data


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
        parsed_data_dict = await get_groq_client().parse_resume(resume_text)

        # Step 2.5: Transform data to fix validation issues
        corrected_data_dict = _transform_parsed_data(parsed_data_dict)
        
        # Step 3: Validate and return structured response
        try:
            validated_data = ResumeData(**corrected_data_dict)
            return ParsedResumeResponse(
                success=True,
                message="Resume parsed successfully",
                data=validated_data
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=422,
                detail=f"Pydantic validation failed after transformation: {e}"
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
