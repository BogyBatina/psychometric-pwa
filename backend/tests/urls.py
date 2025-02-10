from django.urls import path
from .views import get_questions, submit_responses, get_results

# ✅ API Endpoints
urlpatterns = [
    path("questions/", get_questions, name="get_questions"),
    path("submit/", submit_responses, name="submit_responses"),
    path("results/", get_results, name="get_results"),
]
