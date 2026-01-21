"""
Pydantic schemas for the detailed, structured resume data.
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class SocialLinks(BaseModel):
    """Social media links."""
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None


class PersonalInformation(BaseModel):
    """Personal details of the candidate."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    social_links: Optional[SocialLinks] = None


class Education(BaseModel):
    """Education history item."""
    degree: Optional[str] = None
    institution: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[float] = None


class WorkExperience(BaseModel):
    """Work experience item."""
    company: Optional[str] = None
    job_title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    achievements: List[str] = []


class Skills(BaseModel):
    """Categorized skills."""
    technical_skills: List[str] = []
    tools_and_technologies: List[str] = []
    soft_skills: List[str] = []


class Project(BaseModel):
    """Project item."""
    project_name: Optional[str] = None
    description: Optional[str] = None
    technologies_used: List[str] = []


class AdditionalInformation(BaseModel):
    """Additional resume sections."""
    certifications: List[str] = []
    languages: List[str] = []
    awards: List[str] = []


class ResumeData(BaseModel):
    """Root model for the entire structured resume."""
    personal_information: Optional[PersonalInformation] = None
    professional_summary: Optional[str] = None
    education: List[Education] = []
    work_experience: List[WorkExperience] = []
    skills: Optional[Skills] = None
    projects: List[Project] = []
    additional_information: Optional[AdditionalInformation] = None


class ParsedResumeResponse(BaseModel):
    """API response for parsed resume."""
    success: bool
    message: str
    data: Optional[ResumeData] = None
