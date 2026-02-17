from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PersonalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class EducationItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None


class WorkExperienceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: Optional[str] = None
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class SkillSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


class ProjectItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    link: Optional[str] = None


class AdditionalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)


class ResumeSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    personal_information: PersonalInformation = Field(default_factory=PersonalInformation)
    professional_summary: Optional[str] = None
    education: List[EducationItem] = Field(default_factory=list)
    work_experience: List[WorkExperienceItem] = Field(default_factory=list)
    skills: SkillSet = Field(default_factory=SkillSet)
    projects: List[ProjectItem] = Field(default_factory=list)
    additional_information: AdditionalInformation = Field(default_factory=AdditionalInformation)
