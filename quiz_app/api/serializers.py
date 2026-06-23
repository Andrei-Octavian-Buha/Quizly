from rest_framework import serializers
from quiz_app.models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    """
    Full serializer for the Question model.
    
    Used primarily in write/creation pipelines (POST). Includes all fields 
    present in the system, including audit timestamps.
    """
    class Meta:
        model = Question
        fields = ['id','question_title','question_options','answer','created_at','updated_at']

class ListQuestionSerializer(serializers.ModelSerializer):
    """
    Cleaned/Simplified serializer for the Question model.
    
    Exclusively used for fetching data to display on the frontend (GET).
    Omits 'created_at' and 'updated_at' fields for a cleaner UI data payload.
    """
    class Meta:
        model = Question
        fields = ['id','question_title','question_options','answer']

class ListQuizSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for listing and retrieving details of a Quiz.
    
    Maps the nested questions relationship using 'ListQuestionSerializer' (no timestamps)
    and enforces the field to be strictly 'read_only'.
    """
    questions = ListQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields =['id','title','description','created_at','updated_at','video_url','questions']


class QuizSerializer(serializers.ModelSerializer):
    """
    Primary serializer for the Quiz entity, used during write operations.
    
    Handles nested transactional creation for associated questions when 
    the parsed payload arrives from the AI service.
    """
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields =['id','title','description','created_at','updated_at','video_url','questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for q_data in questions_data:
            Question.objects.create(quiz=quiz, **q_data)

        return quiz