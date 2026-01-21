"""
Utility functions for parsing resume files (PDF and DOCX).
"""

import io
from typing import Optional
from fastapi import UploadFile, HTTPException
import pdfplumber
from docx import Document


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text content from PDF file.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        Extracted text as string
        
    Raises:
        HTTPException: If PDF parsing fails
    """
    try:
        content = await file.read()
        text = ""
        
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            raise HTTPException(
                status_code=400, 
                detail="No text could be extracted from the PDF"
            )
        
        return text.strip()
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing PDF: {str(e)}"
        )


async def extract_text_from_docx(file: UploadFile) -> str:
    """
    Extract text content from DOCX file.
    
    Args:
        file: Uploaded DOCX file
        
    Returns:
        Extracted text as string
        
    Raises:
        HTTPException: If DOCX parsing fails
    """
    try:
        content = await file.read()
        doc = Document(io.BytesIO(content))
        
        # Extract text from all paragraphs
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        # Also extract text from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += "\n" + cell.text
        
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the DOCX"
            )
        
        return text.strip()
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing DOCX: {str(e)}"
        )


async def parse_resume_file(file: UploadFile) -> str:
    """
    Parse resume file and extract text based on file type.
    
    Args:
        file: Uploaded resume file (PDF or DOCX)
        
    Returns:
        Extracted text content
        
    Raises:
        HTTPException: If file type is unsupported or parsing fails
    """
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        return await extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        return await extract_text_from_docx(file)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload PDF or DOCX files only."
        )
