from django.urls import path
from .views import (
    get_questions,
    submit_responses,
    get_results,
    get_question_by_id,
    delete_response,
)
from django.views.decorators.csrf import csrf_exempt

# ✅ API Endpoints
urlpatterns = [
    # Retrieve all questions
    path("questions/", get_questions, name="get_questions"),
    
    # Retrieve a specific question by ID (optional, for more flexibility)
    path("questions/<int:question_id>/", get_question_by_id, name="get_question_by_id"),

    # Submit responses (CSRF exempt for API use if needed)
    path("submit/", csrf_exempt(submit_responses), name="submit_responses"),
    
    # Retrieve results
    path("results/", get_results, name="get_results"),

    # Delete a response (useful for admin or debugging)
    path("responses/<int:response_id>/delete/", delete_response, name="delete_response"),
]
