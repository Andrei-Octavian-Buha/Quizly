# Quizly Backend - AI-Powered Quiz Generator

Quizly is a fullstack application that automatically generates educational quizzes from YouTube videos. The backend is built using Django and Django REST Framework (DRF), integrating advanced AI pipelines to handle media downloading, audio transcription, and intelligent question generation.

## 🚀 Tech Stack & Core Libraries

* **Framework:** Django 6.0 & Django REST Framework (DRF)
* **Audio Extraction:** `yt-dlp` (Extracts audio streams directly from YouTube URLs)
* **AI Transcription:** `openai-whisper` (Converts raw audio data into clean text transcripts)
* **LLM Integration:** `google-genai` SDK (Utilizes gemini-2.5-flash to structure transcripts into JSON-formatted quizzes)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)

---

## 🛠️ Installation & Setup

Follow these steps to clone, configure, and run the Quizly Backend locally on your machine.

### Prerequisites
Before installing the Python dependencies, you must ensure that **FFmpeg** is installed on your operating system. It is required by `yt-dlp` to extract and process audio streams from YouTube videos.

* **macOS:** `brew install ffmpeg`
* **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg`
* **Windows:** Download it from the official site or use Chocolatey: `choco install ffmpeg`

### Step-by-Step Instructions

| Action Category | Target Goal | Command / Configuration File |
| :--- | :--- | :--- |
| Repository | Clone the backend repository | `git clone <repository_url>` |
| Project Setup | Change to project directory | `cd Quizly` |
| Environment | Create a Python virtual environment | `python -m venv .venv` |
| Environment | Activate environment (Linux/macOS) | `source .venv/bin/activate` |
| Environment | Activate environment (Windows) | `.venv\Scripts\activate` |
| Dependencies | Install required libraries & packages | `pip install -r requirements.txt` |
| Credentials | Update Gemini API Key inside root folder | Open the existing `config.env` file |
| Database | Create local database structures | `python manage.py migrate` |
| Execution | Launch local development web server | `python manage.py runserver` |

---

## 🔑 Environment Variables Configuration

Before running database migrations or booting up the server, you need to configure your API access.

1. Open the existing `config.env` file located in the root directory of the project (at the exact same level as `manage.py`).
2. Update the `GEMINI_API_KEY` variable with your actual Google Gemini API Key:

```env
# Core API Keys
GEMINI_API_KEY=your_actual_gemini_api_key_here
