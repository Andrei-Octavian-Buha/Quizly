import json
from rest_framework import status, viewsets
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuizSerializer
from quiz_app.models import Quiz
from quiz_app.utils import download_youtube_audio, transcribe_audio_with_whisper, generate_quiz_json

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user).prefetch_related('questions')

    def create(self, request, *args, **kwargs):
        video_url = request.data.get("url")
        if not video_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_path = download_youtube_audio(video_url)
        text_data = transcribe_audio_with_whisper(audio_path)
        ai_raw_json = generate_quiz_json(text_data)

        quiz_data = json.loads(ai_raw_json)
        quiz_data["video_url"] = video_url
        serializer = self.get_serializer(data=quiz_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)