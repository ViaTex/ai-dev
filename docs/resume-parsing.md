# Resume Parsing API - Technical Feature Documentation

## 1. Feature Overview

### Feature Name
Resume Parsing API

### Purpose of the Feature
The Resume Parsing API provides a robust solution for extracting structured data from resumes using a Large Language Model (LLM) integrated with the Groq API. It enables automated parsing of resumes into a predefined JSON schema, making it easier to process and analyze candidate information.

### Problem It Solves
Manual resume parsing is time-consuming and error-prone. This feature automates the process, ensuring accuracy, scalability, and adherence to a strict schema for downstream processing.

### Where It Fits in the Overall System
This feature is part of the backend service, specifically within the `app.api.resume` module. It interacts with the `GroqClient` service for LLM-based parsing and is exposed via RESTful API endpoints.

---

## 2. High-Level Architecture

### Components Involved
- **Frontend**: Not directly involved; can consume the API for displaying parsed resume data.
- **Backend**: FastAPI application handling requests and responses.
- **Services**: `GroqClient` for interacting with the Groq API.
- **Third-party APIs**: Groq API for LLM-based resume parsing.

### Data Flow Explanation
1. A resume file is uploaded via the `/api/parse-resume` endpoint.
2. The file is processed to extract text.
3. The extracted text is sent to the Groq API for parsing.
4. The Groq API returns structured JSON data.
5. The data is validated, transformed, and returned to the client.

### Async/Background Processing
The API uses asynchronous processing for handling file uploads and Groq API interactions to ensure non-blocking operations.

---

## 3. API Documentation

### API Name
Parse Resume

#### HTTP Method
POST

#### Endpoint URL
`/api/parse-resume`

#### Authentication / Authorization
None required.

#### Request Headers
| Header Name      | Description              | Required |
|------------------|--------------------------|----------|
| `Content-Type`   | Must be `multipart/form-data` | Yes      |

#### Request Body
| Field Name       | Type       | Description                     | Required |
|------------------|------------|---------------------------------|----------|
| `file`           | File       | Resume file to be parsed        | Yes      |

#### Example Request (JSON)
```json
{
  "file": "<binary file data>"
}
```

#### Response Structure
| Field Name       | Type       | Description                     |
|------------------|------------|---------------------------------|
| `personal_information` | Object | Parsed personal information |
| `skills`         | Array      | List of extracted skills        |
| `experience`     | Array      | Work experience details         |
| `education`      | Array      | Educational qualifications      |

#### Example Success Response
```json
{
  "personal_information": {
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "location": "New York, USA",
    "social_links": {
      "linkedin": "https://linkedin.com/in/johndoe",
      "github": "https://github.com/johndoe",
      "portfolio": "https://johndoe.com"
    }
  },
  "skills": ["Python", "Machine Learning", "Data Analysis"],
  "experience": [
    {
      "company": "TechCorp",
      "role": "Software Engineer",
      "duration": "Jan 2020 - Dec 2022",
      "description": "Developed scalable backend systems."
    }
  ],
  "education": [
    {
      "institution": "University of Technology",
      "degree": "B.Sc. in Computer Science",
      "year": "2019"
    }
  ]
}
```

#### Example Error Responses
- **Invalid File Format**
```json
{
  "detail": "Unsupported file format. Please upload a valid resume file."
}
```
- **Parsing Error**
```json
{
  "detail": "Failed to parse the resume. Please try again later."
}
```

#### HTTP Status Codes Used
- `200 OK`: Parsing successful.
- `400 Bad Request`: Invalid input.
- `500 Internal Server Error`: Unexpected server error.

#### Validation Rules Applied
- File must be a valid resume format (PDF, DOCX, etc.).
- Maximum file size enforced.

---

## 4. Database / Data Layer

No database is directly involved in this feature. The parsed data is returned to the client without persistent storage.

---

## 5. Algorithms & Logic Used

### Core Algorithms or Methods
- **File Parsing**: Extracts text from uploaded files using PyMuPDF.
- **Prompt Engineering**: Constructs a strict JSON-only prompt for the Groq API.
- **Data Validation**: Ensures the response adheres to the predefined schema.

### Step-by-Step Explanation
1. Extract text from the uploaded file.
2. Construct a JSON-only prompt based on the schema.
3. Send the prompt to the Groq API.
4. Validate and transform the response.

### Edge Cases Handled
- Missing fields in the resume.
- Invalid or unsupported file formats.

---

## 6. Business Logic & Rules

### Important Conditions
- Only valid resume files are accepted.
- The response must strictly adhere to the schema.

### Feature-Specific Rules
- Null values are used for missing fields.
- Empty arrays are used for missing lists.

---

## 7. Error Handling & Edge Cases

### Possible Failure Scenarios
- Invalid file format.
- Groq API errors.
- Network issues.

### How Errors Are Handled
- User-facing errors return descriptive messages.
- Internal errors are logged for debugging.

---

## 8. Security Considerations

### Input Validation
- File type and size are validated.

### Sensitive Data Handling
- No sensitive data is stored.

---

## 9. Performance Considerations

### Optimizations Used
- Asynchronous processing for non-blocking operations.

### Bottlenecks Avoided
- Large file uploads are handled efficiently.

---

## 10. Dependencies

### Internal Modules
- `app.services.groq_client`
- `app.utils.file_parser`

### External Libraries
- `fastapi`
- `httpx`
- `PyMuPDF`

### Third-Party APIs
- Groq API

---

## 11. Configuration & Environment Variables

### Required Env Variables
- `GROQ_API_KEY`: API key for Groq API.
- `MODEL_NAME`: Default model name (optional).

### Default Values
- `MODEL_NAME`: `llama-3.1-8b-instant`

---

## 12. Testing Notes

### Test Cases Covered
- Valid resume file parsing.
- Invalid file format handling.
- Groq API error handling.

### Mocking or Stubbing Used
- Mocked Groq API responses for unit tests.

---

## 13. Future Improvements

### Known Limitations
- No persistent storage for parsed data.

### Scalability Improvements
- Add caching for frequently parsed resumes.

### Refactoring Opportunities
- Modularize the prompt engineering logic.
