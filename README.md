# Quizly Backend - AI-Powered Quiz Generator

Quizly is a fullstack application that automatically generates educational quizzes from YouTube videos. The backend is built using Django and Django REST Framework (DRF), integrating advanced AI pipelines to handle media downloading, audio transcription, and intelligent question generation.

## 🚀 Tech Stack & Core Libraries

* **Framework:** Django 6.0 & Django REST Framework (DRF)
* **Audio Extraction:** `yt-dlp` (Extracts audio streams directly from YouTube URLs)
* **AI Transcription:** `OpenAI Whisper` (Converts raw audio data into clean text transcripts)
* **LLM Integration:** `Google GenAI SDK` (Utilizes `gemini-2.5-flash` to structure transcripts into JSON-formatted quizzes)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)

---

## 🛠️ Installation & Setup

Follow these steps to clone, configure, and run the Quizly Backend locally on your machine.

### Prerequisites

Before installing the Python dependencies, you **must ensure that FFmpeg is installed** on your operating system. It is required by `yt-dlp` to extract and process audio streams from YouTube videos.

* **macOS**: `brew install ffmpeg`
* **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`
* **Windows**: Download it from the official site or use Chocolatey: `choco install ffmpeg`

---

### Step-by-Step Instructions

| Action Category | Target Goal | Command / Configuration File |
| :--- | :--- | :--- |
| **Repository** | Clone the backend repository | `git clone <repository_url>` |
| **Project Setup** | Change to project directory | `cd Quizly` |
| **Environment** | Create a Python virtual environment | `python -m venv .env` |
| **Environment** | Activate environment (Linux/macOS) | `source .env/bin/activate` |
| **Environment** | Activate environment (Windows) | `.env\Scripts\activate` |
| **Dependencies** | Install required libraries & packages | `pip install -r requirements.txt` |
| **Credentials** | Configure API access inside root folder | Create **`config.env`** at the same level as `manage.py` |
| **Database** | Create local database structures | `python manage.py migrate` |
| **Execution** | Launch local development web server | `python manage.py runserver` |

---

### 🔑 Environment Variables Configuration

Before running database migrations or booting up the server, you need to set up your local environment configurations. 

1. Create a file named **`config.env`** in the root directory of the project (at the exact same level as `manage.py`).
2. Open the file and add your configuration details:

```env
# Core API Keys
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Django Settings
DEBUG=True
```

⚠️ Security Warning: Never commit your config.env file to public repositories like GitHub. Ensure it is included in your .gitignore file.


🚀 Verifying the Server

Once you execute the server execution setup steps, open your browser or API testing environment and point it to:
Plaintext
```Plaintext
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
```


To easily view your data in a graphical dashboard, you can optionally provision a management profile to log into the Django Administration Interface (http://127.0.0.1:8000/admin/) by executing:
```Bash
python manage.py createsuperuser
```
