# Resume Parsing AI Service

Production-grade, stateless resume parsing microservice built with FastAPI, LangChain, and Groq.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:

```bash
GROQ_API_KEY=your_groq_key
INTERNAL_API_KEY=your_internal_key
MAX_FILE_SIZE_MB=5
ALLOWED_FILE_TYPES=pdf,docx
```

4. Run locally:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker

Build and run:

```bash
docker build -t ai-resume-service .
docker run --rm -p 8000:8000 --env-file .env ai-resume-service
```

## Endpoints

- `POST /resume-parse`
- `GET /health`
- `GET /ready`

## Example Request

```bash
curl -X POST http://localhost:8000/resume-parse \
  -H "X-Internal-API-Key: your_key" \
  -F "user_id=uuid-value" \
  -F "file=@resume.pdf"
```
