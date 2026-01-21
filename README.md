# Resume Parsing API Prototype

This project is a beginner-friendly prototype for a resume parsing service built with FastAPI. It uses the Groq API to perform LLM-based extraction of structured data from PDF and DOCX resume files.

## 1. Project Overview

The goal of this project is to provide a simple yet functional API that can:
- Accept resume file uploads (PDF and DOCX).
- Extract raw text from the files.
- Use a Large Language Model (LLM) to parse the text into a structured JSON format.
- Return the structured data to the user.

This prototype is designed to be easy to understand, set up, and run, making it a great starting point for more complex NLP projects.

## 2. Tech Stack

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **LLM Provider:** [Groq](https://groq.com/)
- **File Parsing:**
  - `pdfplumber` for PDF files
  - `python-docx` for DOCX files
- **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
- **Environment Variables:** `python-dotenv`
- **HTTP Client:** `httpx`

## 3. Folder Structure

The project follows a simple and intuitive folder structure:

```
.
├── app
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── api
│   │   ├── __init__.py
│   │   └── resume.py     # API endpoints
│   ├── services
│   │   ├── __init__.py
│   │   └── groq_client.py  # Groq API integration
│   ├── utils
│   │   ├── __init__.py
│   │   └── file_parser.py  # PDF and DOCX text extraction
│   └── schemas
│       ├── __init__.py
│       └── resume_schema.py # Pydantic data models
│
├── docs
│   └── resume-parsing.md # Technical documentation
│
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md
```

## 4. Setup and Installation

Follow these steps to get the project running locally.

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd dishasetu-ai
```

### Step 2: Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

The application requires API keys and configuration to be stored in a `.env` file.

1.  Make a copy of the `.env.example` file (if provided) or create a new file named `.env` in the project root.
2.  Open the `.env` file and add your Groq API key:

    ```env
    # .env

    # Groq API Configuration
    GROQ_API_KEY=your_groq_api_key_here
    MODEL_NAME=mixtral-8x7b-32768
    ```

    - You can get a free Groq API key from the [Groq Console](https://console.groq.com/keys).
    - `mixtral-8x7b-32768` is a good default model, but you can experiment with others like `llama-3.1-70b-versatile`.

## 5. How to Run the Server

Once the setup is complete, you can run the FastAPI server using Uvicorn.

```bash
uvicorn app.main:app --reload
```

- `uvicorn`: The ASGI server that runs the application.
- `app.main:app`: Tells Uvicorn where to find the FastAPI app instance (`app` in `app/main.py`).
- `--reload`: Enables auto-reloading, so the server will restart automatically after code changes.

The server will start on `http://127.0.0.1:8000`.

## 6. API Usage

You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### Parse a Resume

- **Endpoint:** `POST /api/parse-resume`
- **Description:** Upload a resume file to extract structured data.
- **Body:** `multipart/form-data` with a `file` field containing the PDF or DOCX file.

#### Example Request using `curl`

```bash
curl -X POST "http://127.0.0.1:8000/api/parse-resume" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/resume.pdf"
```

Replace `/path/to/your/resume.pdf` with the actual path to your resume file.

#### Example Success Response (Updated)

The API returns a detailed JSON object that strictly follows the defined schema.

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

For more detailed technical information, please see the [technical documentation](./docs/resume-parsing.md).
