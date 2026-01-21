# Technical Documentation: LLM-Based Resume Parsing Prototype

**Author:** AI Assistant
**Date:** 2026-01-21
**Status:** Initial Draft

## 1. Overview

This document outlines the architecture and implementation of the LLM-based resume parsing prototype. The goal of this project is to quickly build a functional service that can extract structured data from resume files (PDF and DOCX) using a Large Language Model (LLM).

This approach was chosen for its rapid development cycle and flexibility, making it ideal for a prototype where the primary goal is to validate the end-to-end workflow of resume processing.

## 2. Why LLM-Based Parsing?

Traditional resume parsing relies on complex NLP pipelines involving rule-based systems, statistical models, or custom-trained machine learning models. While powerful, these systems are time-consuming and expensive to build and maintain.

For this prototype, we chose an LLM-based approach for several key reasons:

- **Speed of Development:** Using a pre-trained LLM like Mixtral or Llama via the Groq API allows us to achieve sophisticated parsing capabilities with minimal code and no model training.
- **Flexibility:** LLMs are highly adaptable. They can handle a wide variety of resume formats and layouts without needing to be explicitly programmed for each one.
- **Cost-Effectiveness (for Prototyping):** While API calls have a cost, it is significantly lower than the cost of R&D, data annotation, and infrastructure for a custom NLP pipeline, especially in the early stages.
- **Focus on Core Logic:** This approach allows us to focus on the application's business logic (file handling, API design, data storage) rather than getting bogged down in the complexities of NLP.

## 3. System Architecture

The system is a simple FastAPI application with a clear, single-purpose design.

![System Architecture Diagram](https://i.imgur.com/example.png)  <!-- Placeholder for a real diagram -->

The workflow is as follows:
1. A user uploads a resume file (PDF or DOCX) to the `/api/parse-resume` endpoint.
2. The `file_parser` utility extracts the raw text content from the file.
3. The extracted text is passed to the `groq_client` service.
4. The `groq_client` constructs a detailed prompt, instructing the LLM to return a structured JSON object.
5. The Groq API processes the text and returns a JSON response.
6. The application validates the JSON response using a Pydantic schema and returns it to the user.

## 4. Resume Text Extraction

The first step in the pipeline is to get clean, raw text from the uploaded resume. We support two common formats: PDF and DOCX.

### 4.1. PDF Parsing (`pdfplumber`)

We use the `pdfplumber` library for PDF text extraction. It was chosen over `PyPDF2` because it is generally better at preserving the layout and reading order of text, which is crucial for the LLM to understand the context.

The `extract_text_from_pdf` function reads the file content, opens it with `pdfplumber`, and iterates through each page to extract text.

### 4.2. DOCX Parsing (`python-docx`)

For DOCX files, we use the `python-docx` library. It allows us to extract text from both paragraphs and tables, ensuring that no information is missed. The `extract_text_from_docx` function iterates through all paragraphs and table cells to build the full text content.

## 5. Groq API Integration and Prompt Design

The core of the parsing logic lies in the interaction with the Groq API.

### 5.1. Groq Client

The `GroqClient` class in `groq_client.py` encapsulates all interaction with the Groq API. It handles:
- Loading the `GROQ_API_KEY` and `MODEL_NAME` from environment variables.
- Constructing the API request with appropriate headers and payload.
- Making the asynchronous HTTP request using `httpx`.
- Handling API errors and parsing the response.

### 5.2. Prompt Design Strategy: Schema-Driven Parsing

The prompt is the most critical component of this system. A well-designed prompt is the key to getting accurate, structured, and reliable output from the LLM. Our strategy has evolved to be **schema-driven**.

Instead of a loose set of instructions, we provide the LLM with a strict JSON schema that it must follow. This approach significantly improves the reliability and consistency of the output.

Our prompt strategy includes several key elements:
- **Role-Playing:** The prompt starts with `You are an expert resume parsing AI.`, which sets the context for the LLM.
- **Forced JSON Output:** We explicitly instruct the model to `return ONLY a valid JSON object` and provide a detailed example of the required JSON structure, including all fields and data types.
- **Strict Schema Adherence:** The prompt emphasizes that the model must not add, remove, or rename any fields from the provided schema.
- **Handling Missing Data:** The prompt specifies that the model should use `null` for missing single values and `[]` for missing lists. This ensures a consistent output schema, which can be reliably validated by our Pydantic models.
- **Low Temperature:** We set the `temperature` parameter to `0.1`. A low temperature makes the model's output more deterministic and less "creative," which is essential for reliable data extraction.

This schema-driven approach makes the LLM's behavior more predictable and treats it as a structured data transformation engine rather than a creative text generator.

## 6. New Extraction Fields and JSON Structure

The data extraction capabilities have been significantly enhanced to capture a more detailed and structured view of the resume.

### 6.1. Full JSON Schema

The API now returns a JSON object with the following structure:

-   `personal_information`:
    -   `full_name`, `email`, `phone`, `location`
    -   `social_links`: `linkedin`, `github`, `portfolio`
-   `professional_summary`: A string containing the resume's objective or summary.
-   `education`: An array of objects, each with `degree`, `institution`, `start_date`, `end_date`, and `gpa`.
-   `work_experience`: An array of objects, each with `company`, `job_title`, `start_date`, `end_date`, `description`, and an array of `achievements`.
-   `skills`: An object containing arrays for `technical_skills`, `tools_and_technologies`, and `soft_skills`.
-   `projects`: An array of objects, each with `project_name`, `description`, and an array of `technologies_used`.
-   `additional_information`: An object containing arrays for `certifications`, `languages`, and `awards`.

### 6.2. Example API Output

A successful response will have a `200 OK` status code and a JSON body like this:

```json
{
  "success": true,
  "message": "Resume parsed successfully",
  "data": {
    "personal_information": {
      "full_name": "Rahul Bastia",
      "email": "rahul.bastia00@gmail.com",
      "phone": "+91-6371480952",
      "location": null,
      "social_links": {
        "linkedin": "https://www.linkedin.com/",
        "github": "https://github.com/",
        "portfolio": "https://www.codolio.com/"
      }
    },
    "professional_summary": null,
    "education": [
      {
        "degree": "Bachelor of Technology - Computer Science (Artificial Intelligence)",
        "institution": "Gandhi Institute for Technology Autonomous (GIFT) Bhubaneswar, India",
        "start_date": "2022",
        "end_date": "2026",
        "gpa": null
      }
    ],
    "work_experience": [
      {
        "company": "SakRobotics Lab Pvt. Ltd.",
        "job_title": "AI & Robotics (Intern)",
        "start_date": "Sep 2025",
        "end_date": "Dec 2025",
        "description": null,
        "achievements": [
          "Vision-Based Teleoperation Pipeline: Engineered a teleoperation system using MediaPipe and Inverse Kinematics; eliminated servo jitter via adaptive signal filtering.",
          "Python–Arduino Data Sync: Built a synchronized Python-Arduino interface to align video and motor streams, generating high-quality datasets for Imitation Learning.",
          "Optimized Hardware Communication: Enhanced I2C-based communication, reducing system latency and enabling real-time, responsive robotic control."
        ]
      }
    ],
    "skills": {
      "technical_skills": [
        "Python",
        "Java",
        "SQL",
        "KQL",
        "C"
      ],
      "tools_and_technologies": [
        "PyTorch",
        "TensorFlow",
        "Keras",
        "Scikit-learn",
        "LangChain",
        "LangGraph",
        "LightGBM",
        "OpenCV",
        "Pandas",
        "NumPy",
        "Microsoft Fabric",
        "Lakehouse Architecture",
        "Delta Lake",
        "Apache Spark",
        "PySpark",
        "PostgreSQL",
        "MySQL",
        "PGVector (Vector DB)",
        "Docker",
        "FastAPI",
        "Google Cloud Platform (GCP)",
        "Git",
        "GitHub Actions",
        "CI/CD",
        "Power BI",
        "Matplotlib",
        "Seaborn",
        "Exploratory Data Analysis (EDA)"
      ],
      "soft_skills": []
    },
    "projects": [
      {
        "project_name": "Aadhaar Drishti: Predictive Governance & Risk Engine",
        "description": null,
        "technologies_used": [
          "PySpark",
          "Facebook Prophet",
          "Microsoft Fabric",
          "Pandas",
          "Seaborn"
        ]
      },
      {
        "project_name": "Context-Aware Price Modeling (Amazon ML Challenge)",
        "description": null,
        "technologies_used": [
          "Python",
          "OpenAI CLIP",
          "GNN",
          "LightGBM",
          "FAISS"
        ]
      },
      {
        "project_name": "Autonomous Financial Analysis Agent",
        "description": null,
        "technologies_used": [
          "Python",
          "LangChain",
          "FastAPI",
          "Docker",
          "PostgreSQL"
        ]
      }
    ],
    "additional_information": {
      "certifications": [],
      "languages": [],
      "awards": [
        "1st Place – Hackfest 2025 : Led development of an AI-driven route-optimization engine, outperforming 300+ teams and reducing simulated vehicle emissions.",
        "Top 5 – Trithon 2025: Ranked among 3,000+ developers for optimizing AI inference pipelines and algorithmic efficiency.",
        "Algorithmic Problem Solving: Solved 150+ DSA problems on LeetCode and GFG Practice with focus on graph algorithms and dynamic programming."
      ]
    }
  }
}
```

## 7. Limitations and Future Improvements


This prototype is highly effective for its intended purpose, but it has limitations that should be understood.

### 7.1. Limitations

- **Dependency on External API:** The system's performance and availability are tied to the Groq API.
- **Cost at Scale:** While cheap for a prototype, API calls can become expensive at a high volume.
- **Lack of Control:** We have limited control over the underlying model. Changes to the model by the provider could potentially affect parsing accuracy.
- **Potential for "Hallucinations":** LLMs can occasionally invent or misinterpret information, although our prompt is designed to minimize this.
- **Data Privacy:** Sending resume data to a third-party API may not be acceptable for all use cases.

### 7.2. Future Improvements: Evolving to a Production NLP Pipeline

This prototype serves as a great starting point. A future, production-grade system would likely replace the LLM API call with a more robust, in-house NLP pipeline. This could involve:

1. **Hybrid Approach:** Continue using the LLM for its flexibility but add a validation and correction layer, possibly with human review for a small percentage of resumes.
2. **Fine-Tuning a Model:** Fine-tune a smaller, open-source model (like a BERT variant) on a dataset of annotated resumes. This provides more control and can be hosted internally.
3. **Rule-Based Pre-processing:** Use regular expressions and rule-based systems to extract highly structured information like emails and phone numbers before sending the rest of the text to a model.
4. **Building a Full-Scale NLP Pipeline:** For maximum accuracy and control, a full pipeline could be built, involving:
   - **Text Cleaning and Normalization.**
   - **Named Entity Recognition (NER)** to identify entities like names, companies, and skills.
   - **Relation Extraction** to link entities (e.g., linking a position to a company).
   - **Classification** to categorize skills or job descriptions.

By starting with this LLM-based prototype, we can gather data, refine requirements, and deliver value quickly, while planning a strategic transition to a more sophisticated solution as the need arises.
