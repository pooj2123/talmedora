# TALMedora

## AI-Powered Medical Report Assistant

TALMedora is a secure AI-powered healthcare assistant that allows users to upload medical reports, store them safely, and interact with an AI assistant that answers questions based only on their own uploaded reports.

---

## Features

### Authentication & Security

* User Registration
* User Login
* JWT Authentication
* Password Hashing
* Protected Routes
* User-specific Report Access
* Secure Report Download
* Secure Report Deletion
* User-Isolated AI Retrieval

---

### Medical Report Management

* Upload PDF Medical Reports
* Store Metadata in SQLite
* View Uploaded Reports
* Download Reports
* Delete Reports
* Search Reports

---

### AI Assistant

* AI-powered medical report Q&A
* FAISS Vector Database
* Semantic Search
* Gemini Integration
* User-specific document retrieval
* Retrieval-Augmented Generation (RAG)

---

## System Architecture

```text
Frontend (React + Tailwind)
        |
        v
Backend (FastAPI)
        |
        +---- JWT Authentication
        |
        +---- SQLite Database
        |
        +---- FAISS Vector Store
        |
        +---- Gemini AI
```

---

## Tech Stack

### Frontend

* React
* React Router
* Axios
* Tailwind CSS

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication

### AI & NLP

* Google Gemini
* LangChain
* FAISS
* Sentence Transformers

---

## Folder Structure

```text
ai-report-assistant/

├── backend/
│   ├── auth/
│   ├── database/
│   ├── routes/
│   ├── services/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
│
└── README.md
```

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Backend

```bash
python -m uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Frontend Setup

### Install Packages

```bash
npm install
```

### Start Frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## Security Features

### User Isolation

Users can only:

* View their own reports
* Download their own reports
* Delete their own reports
* Chat with their own report data

### AI Data Protection

Each document chunk stored in FAISS contains:

```python
{
    "user_id": user.id
}
```

AI retrieval filters results using the authenticated user's ID before generating responses.

---

## Future Enhancements

* AI Medical Report Summaries
* OCR for Image Reports
* Dashboard Analytics
* Chat History
* Doctor Recommendation Engine
* Multi-language Support
* Cloud Deployment

---

## Authors

Developed as part of an AI-powered healthcare assistant project.

Project Name: TALMedora
