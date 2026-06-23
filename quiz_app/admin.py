from django.contrib import admin
from .models import Quiz, Question

class QuestionInline(admin.TabularInline):
    """
    Allows questions to be edited directly inside the Quiz admin page.
    """
    model = Question
    extra = 1  # Number of empty slots to display for new questions
    fields = ['question_title', 'question_options', 'answer']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Quiz model.
    """
    list_display = ['id', 'title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model (optional, for standalone viewing).
    """
    list_display = ['id', 'quiz', 'question_title', 'created_at']
    list_filter = ['quiz', 'created_at']
    search_fields = ['question_title']