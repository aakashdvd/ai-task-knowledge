# AI Task & Knowledge Management System

A minimal full stack MVP where an admin uploads knowledge documents and assigns tasks, while users search the knowledge base using semantic search and complete assigned tasks.

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- MySQL
- JWT authentication
- ChromaDB
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Optional Gemini for grounded answer generation

### Frontend
- React
- Vite
- Axios
- React Router

## Core Features

- JWT authentication with Admin and User roles
- Role based API protection
- Task creation, listing, filtering, and completion
- `.txt` document upload and chunking
- Embedding based semantic search using ChromaDB
- Activity logging for login, upload, search, and task updates
- Basic analytics for tasks, searches, and documents
- Optional grounded Gemini answer generation on top of retrieved chunks

## Project Structure

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    utils/
  scripts/

frontend/
  src/
    api/
    components/
    context/
    pages/
```

## Setup Steps
### 1. Clone the repositor
```
git clone https://github.com/<your-username>/ai-task-knowledge.git
cd ai-task-knowledge
```

### 2. Backend Setup
```
cd backend
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Update .env with your MySQL credentials and optional Gemini key.

Create the MySQL database:
```
CREATE DATABASE ai_task_knowledge
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```
Seed demo users:
```
python -m scripts.seed
```

Run the backend:
```
uvicorn app.main:app --reload
```

Optional backfill for older uploaded documents:
```
python -m scripts.backfill_chroma
```

### 3. Frontend Setup 
Open a new terminal
```
cd frontend
npm install
copy .env.example .env
npm run dev
```
## Demo Credentials

### Admin
  * Email: admin@example.com
  * Password: Admin@123
### User
  * Email: user@example.com
  * Password: User@123
### Required APIs
  *POST /auth/login
  *POST /tasks
  *GET /tasks
  *POST /documents
  *GET /documents
  *POST /search
  *GET /analytics

## Short Explanation

This system stores structured application data in MySQL and semantic knowledge representations in ChromaDB. Uploaded text documents are chunked and embedded using a sentence-transformer model. Search queries are embedded in the same vector space and matched against stored document chunks. This allows users to retrieve relevant knowledge passages and complete assigned tasks using the uploaded information.

Gemini is optional and used only after retrieval to generate a grounded answer from the retrieved chunks. The main search logic remains embedding-based and does not depend solely on an LLM API.

## Notes

* .txt upload is supported in this MVP. PDF can be added later.
* uploads/ and chroma_store/ are runtime folders and are not committed.
* Search analytics include both successful and unsuccessful user queries.

