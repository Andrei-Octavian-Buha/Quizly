import json
from rest_framework import status, viewsets
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuizSerializer, ListQuizSerializer
from .permissions import IsQuizOwner
from quiz_app.models import Quiz
from quiz_app.utils import download_youtube_audio, transcribe_audio_with_whisper, generate_quiz_json

class QuizViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Quiz models.
    
    Provides support for listing, creating, retrieving details, partially updating,
    and deleting quizzes, ensuring strict data isolation between users.
    """
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsQuizOwner]

    def get_queryset(self):
        """
        Returns the optimized queryset based on the current HTTP action.
        
        For the 'list' action, it returns only the quizzes belonging to the authenticated user.
        For all other actions, it returns all records to allow permission classes to 
        properly evaluate access rights and return accurate HTTP status codes (403 vs 404).
        """
        if self.action == 'list':
            return Quiz.objects.filter(user=self.request.user).prefetch_related('questions')
        return Quiz.objects.all().prefetch_related('questions')
    
    def get_serializer_class(self):
        """
        Dynamically selects the serializer class based on the current HTTP action.
        
        Returns ListQuizSerializer for GET requests (list, retrieve) to omit question 
        timestamps, and QuizSerializer for all other mutation operations.
        """
        if self.action in ['list', 'retrieve']:
            return ListQuizSerializer
        return QuizSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Generates a new quiz based on a provided YouTube URL.
        
        The background process downloads the audio track, transcribes it via Whisper,
        parses the text into quiz questions using AI, and persists the data structure.
        
        The successful response (201 Created) includes timestamps for both the quiz and its questions.
        """
        video_url = request.data.get("url")
        if not video_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_path = download_youtube_audio(video_url)
        text_data = transcribe_audio_with_whisper(audio_path)
        ai_raw_json = generate_quiz_json(text_data)
        try:
            quiz_data = json.loads(ai_raw_json)
        except:
            return Response(
                {"error": "AI service is temporarily busy. Please try again in a few moments."}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        quiz_data["video_url"] = video_url
        serializer = self.get_serializer(data=quiz_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)