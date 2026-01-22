"""
Groq API client for LLM-based resume parsing.
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
        """Build a strict JSON-only resume parsing prompt."""

        return f"""
You are an expert resume parsing engine.

CRITICAL RULES:
1. Output ONLY valid JSON
2. Do NOT include explanations or markdown
3. Do NOT hallucinate information
4. Use null for missing values
5. Use [] for missing lists
6. Follow the schema EXACTLY

JSON SCHEMA:
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

RESUME TEXT:
----------------
{resume_text}
----------------

Return ONLY the JSON object.
""".strip()

    async def parse_resume(self, resume_text: str) -> dict:
        """Send resume text to Groq API and return raw parsed data as a dictionary."""

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
            "max_tokens": 2000,
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

            # Safety: remove markdown if model adds it
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            parsed_json = json.loads(content)
            return parsed_json  # Return raw dict for transformation in the API layer

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
groq_client = GroqClient()
