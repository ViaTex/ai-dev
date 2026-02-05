"""
Groq API client for LLM-based resume parsing.
Merged prompt: high-fidelity, ATS-safe, non-hallucinating resume extraction.
"""

import os
import json
import httpx
from fastapi import HTTPException


class GroqClient:
    """Client for interacting with Groq API."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        if not self.api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. "
                "Ensure .env is loaded and the server was restarted."
            )

    def _build_parsing_prompt(self, resume_text: str) -> str:
        """
        Build a strict, high-fidelity JSON-only resume parsing prompt.
        Combines structural rigor + semantic richness without hallucination.
        """

        return f"""
You are a Senior Recruitment Data Architect and an Expert Resume Parsing Engine.

Your task is to transform unstructured resume text into a structured, high-fidelity JSON object
for use in ATS systems, talent intelligence platforms, and professional profile builders.

========================
CRITICAL OUTPUT RULES
========================
1. Output ONLY valid JSON
2. Do NOT include explanations, markdown, or comments
3. Do NOT hallucinate or infer information not explicitly stated
4. Use null for missing string values
5. Use [] for missing lists
6. Follow the JSON schema EXACTLY
7. Preserve all meaningful technical detail — do NOT over-summarize
8. Never fabricate skills, metrics, dates, or achievements

========================
EXTRACTION & NORMALIZATION LOGIC
========================

DATE HANDLING:
- Preserve dates exactly as stated in the resume
- Convert to readable format when possible (e.g., "Sep 2025")
- Use "Present" ONLY if the resume explicitly indicates an ongoing role or degree
- Do NOT assume ongoing status

EDUCATION:
- Preserve full institution names, INCLUDING location if present
- Do not shorten institution names
- Do not infer GPA if not stated

WORK EXPERIENCE:
- Extract only professional roles (internships, jobs, contracts)
- description:
  - 1–2 line high-level responsibility summary (no links, no labels like "(Video)")
- achievements:
  - Bullet-level, concrete accomplishments
  - Include metrics, systems, models, optimizations, or outcomes when explicitly stated

PROJECTS:
- Include academic, personal, hackathon, or research projects
- Preserve multi-paragraph technical depth if present
- Do NOT truncate models, pipelines, algorithms, or system design details

SKILL TAXONOMY (STRICT):
- technical_skills:
  - Core concepts (e.g., Data Structures, Object-Oriented Programming, Machine Learning, SEO)
- tools_and_technologies:
  - Languages, frameworks, platforms, databases, libraries
- soft_skills:
  - Behavioral or leadership traits ONLY if explicitly stated

SOCIAL LINKS:
- Extract COMPLETE URLs when present
- If only a username is present, construct full URLs:
  - LinkedIn: https://linkedin.com/in/{{username}}
  - GitHub: https://github.com/{{username}}
- If not present, use null

========================
JSON SCHEMA (MUST MATCH EXACTLY)
========================
{{
  "personal_information": {{
    "full_name": null,
    "email": null,
    "phone": null,
    "location": null,
    "social_links": {{
      "linkedin": null,
      "github": null,
      "portfolio": null
    }}
  }},
  "professional_summary": null,
  "education": [
    {{
      "degree": null,
      "institution": null,
      "start_date": null,
      "end_date": null,
      "gpa": null
    }}
  ],
  "work_experience": [
    {{
      "company": null,
      "job_title": null,
      "start_date": null,
      "end_date": null,
      "description": null,
      "achievements": []
    }}
  ],
  "skills": {{
    "technical_skills": [],
    "tools_and_technologies": [],
    "soft_skills": []
  }},
  "projects": [
    {{
      "project_name": null,
      "description": null,
      "technologies_used": []
    }}
  ],
  "additional_information": {{
    "certifications": [],
    "languages": [],
    "awards": []
  }}
}}

========================
RESUME TEXT
========================
{resume_text}

Return ONLY the JSON object.
""".strip()

    async def parse_resume(self, resume_text: str) -> dict:
        """Send resume text to Groq API and return parsed JSON as a dictionary."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a strict JSON-only resume parsing engine.",
                },
                {
                    "role": "user",
                    "content": self._build_parsing_prompt(resume_text),
                },
            ],
            "temperature": 0.1,
            "max_tokens": 2200,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Groq API error: {response.text}",
                )

            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()

            # Safety cleanup if model adds code fences
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            parsed_json = json.loads(content)
            return parsed_json

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Groq returned invalid JSON output",
            )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to Groq API: {str(e)}",
            )


# Singleton instance
_groq_client_instance = None


def get_groq_client() -> GroqClient:
    """Get or create the Groq client instance (lazy initialization)."""
    global _groq_client_instance
    if _groq_client_instance is None:
        _groq_client_instance = GroqClient()
    return _groq_client_instance
