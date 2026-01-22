# Technical Documentation: LLM-Based Resume Parsing Prototype

**Author:** AI Assistant
**Date:** 2026-01-21
**Status:** Initial Draft

## 1. Overview

This document describes an LLM-based resume parsing prototype designed to extract structured information from PDF and DOCX resumes. The system prioritizes rapid development and flexibility, making it suitable for validating the end-to-end resume processing workflow during early-stage development.

## 2. Rationale for LLM-Based Parsing

Traditional resume parsing systems rely on complex NLP pipelines that require significant development time and maintenance. For a prototype, an LLM-based approach offers clear advantages:

* **Rapid Development:** Pre-trained LLMs accessed via the Groq API enable advanced parsing without model training.
* **Format Flexibility:** The system adapts well to diverse resume layouts and writing styles.
* **Lower Initial Cost:** API usage is more economical than building and maintaining a custom NLP pipeline at the prototyping stage.
* **Focus on Core Architecture:** Development effort is concentrated on file handling, API design, and data validation rather than NLP internals.

## 3. System Architecture

The system is implemented as a lightweight FastAPI service with a single responsibility: resume parsing.

**Workflow:**

1. A resume file is uploaded to the `/api/parse-resume` endpoint.
2. Raw text is extracted using a format-specific parser.
3. The extracted text is sent to the Groq API via a dedicated client.
4. The LLM returns structured JSON based on a predefined schema.
5. The response is validated using Pydantic and returned to the client.

## 4. Resume Text Extraction

### 4.1 PDF Parsing (`pdfplumber`)

`pdfplumber` is used for PDF text extraction due to its superior handling of layout and reading order compared to alternatives such as `PyPDF2`.

### 4.2 DOCX Parsing (`python-docx`)

`python-docx` is used to extract text from both paragraphs and tables, ensuring complete coverage of document content.

## 5. Groq API Integration and Prompt Design

### 5.1 Groq Client

The `GroqClient` module manages API communication, including:

* Environment-based configuration
* Request construction and execution
* Error handling and response parsing

### 5.2 Schema-Driven Prompting

The system uses a strict, schema-driven prompt strategy to improve reliability:

* The LLM is instructed to return **only valid JSON**
* A fixed schema defines all fields and data types
* Missing values are represented as `null` or empty arrays
* Low temperature (`0.1`) is used to reduce output variance

This approach treats the LLM as a deterministic data extraction engine rather than a generative model.

## 6. Extracted Data Structure

The API returns structured resume data, including:

* **Personal Information:** name, contact details, social links
* **Professional Summary**
* **Education**
* **Work Experience** with achievements
* **Skills:** technical, tools, soft skills
* **Projects**
* **Additional Information:** certifications, languages, awards

All fields follow a consistent JSON schema suitable for validation and downstream processing.

## 7. Limitations and Future Enhancements

### 7.1 Current Limitations

* Dependency on an external API
* Increased cost at scale
* Limited control over model behavior
* Occasional risk of hallucinated data
* Data privacy considerations for third-party processing

### 7.2 Future Direction

A production-ready system may evolve toward:

* Hybrid LLM + rule-based validation
* Fine-tuned, self-hosted models
* Regex-based pre-extraction for structured fields
* Full NLP pipelines with NER, relation extraction, and classification

This prototype provides a fast and effective foundation while enabling informed planning for a scalable, production-grade solution.

---

