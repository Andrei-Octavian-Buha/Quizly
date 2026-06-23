import os 
import whisper
from google import genai
from yt_dlp import YoutubeDL

def download_youtube_audio(url : str) -> str:
    """
    Downloads the audio stream from a given YouTube video URL.

    Args:
        url (str): The full URL of the YouTube video.

    Returns:
        str: The local file path where the extracted MP3 audio is temporarily saved.
    """
    with YoutubeDL({"quiet": True}) as ydl:
        video_id = ydl.extract_info(url, download=False)["id"]
    tmp_filename = f"downloads/{video_id}.mp3"

    ydl_opts = {
        "format" : "bestaudio/best",
        "outtmpl" : tmp_filename,
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return tmp_filename
    
def transcribe_audio_with_whisper(file_path: str) -> str:
    """
    Transcribes a local audio file into raw text using OpenAI's Whisper model.
    Automatically deletes the temporary audio file after successful transcription.

    Args:
        file_path (str): The local system path to the audio file.

    Returns:
        str: The processed text transcript of the audio file.
    """
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    return result["text"]

def generate_quiz_json(transcript: str) -> str:
    """
    Sends the raw transcript text to Gemini 2.5 Flash to generate a structured quiz.

    Args:
        transcript (str): The text transcript extracted from the video.

    Returns:
        str: A raw, valid JSON string containing a title, description, and an array 
             of exactly 10 multiple-choice questions with 4 options and the correct answer.
    """
    client = genai.Client()
    prompt = f"Create q quiz with 10 multiple-choice questions from this text : {transcript}"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={    
            'response_mime_type': 'application/json',
            'system_instruction': (
                "Output a raw JSON object matching this schema exactly: "
                "{'title': str, 'description': str, 'questions': ["
                "{'question_title': str, 'question_options': [str, str, str, str], 'answer': str}]}"
            )
        }   
    )

    return response.text