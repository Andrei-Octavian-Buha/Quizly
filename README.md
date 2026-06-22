# Quizly Backend - AI-Powered Quiz Generator

Quizly is a fullstack application that automatically generates educational quizzes from YouTube videos. The backend is built using Django and Django REST Framework (DRF), integrating advanced AI pipelines to handle media downloading, audio transcription, and intelligent question generation.

## 🚀 Tech Stack & Core Libraries

* **Framework:** Django 6.0 & Django REST Framework (DRF)
* **Audio Extraction:** `yt-dlp` (Extracts audio streams directly from YouTube URLs)
* **AI Transcription:** `OpenAI Whisper` (Converts raw audio data into clean text transcripts)
* **LLM Integration:** `Google GenAI SDK` (Utilizes `gemini-2.5-flash` to structure transcripts into JSON-formatted quizzes)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)

---

## 🛠️ Step-by-Step Project Instructions

| Action Category | Target Goal | Command / Configuration File |
| :--- | :--- | :--- |
| **Project Setup** | Change to project directory | `cd quizly` |
| **Environment** | Create a Python virtual environment | `python -m venv .env` |
| **Environment** | Activate environment (Linux/macOS) | `source .env/bin/activate` |
| **Environment** | Activate environment (Windows) | `.env\Scripts\activate` |
| **Dependencies** | Install required libraries & packages | `pip install -r requirements.txt` |
| **Credentials** | Configure API access inside root folder | Create **`config.env`** containing `GEMINI_API_KEY=your_key` |
| **Database** | Create local database structures | `python manage.py migrate` |
| **Execution** | Launch local development web server | `python manage.py runserver` |

---

## 📌 API Endpoints Contract

All endpoints require Token/Session Authentication. Users can only access, modify, or delete their own quizzes.

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/quizzes/` | Creates a new quiz from a YouTube URL via AI pipeline. | `201`, `400`, `401`, `500` |
| **GET** | `/api/quizzes/` | Retrieves a list of all quizzes created by the user. | `200`, `401`, `500` |
| **GET** | `/api/quizzes/{id}/` | Retrieves details and questions for a specific quiz. | `200`, `401`, `403`, `404`, `500` |
| **PATCH** | `/api/quizzes/{id}/` | Partially updates quiz details (e.g., Title, Description). | `200`, `400`, `401`, `403`, `404`, `500` |
| **DELETE** | `/api/quizzes/{id}/` | Permanently deletes a quiz and its linked questions. | `204`, `401`, `403`, `404`, `500` |

---

## 📋 Request/Response Payload Examples

### 1. Create a Quiz (`POST /api/quizzes/`)

**Request Body:**
```json
{
  "url": "[https://www.youtube.com/watch?v=example](https://www.youtube.com/watch?v=example)"
}
