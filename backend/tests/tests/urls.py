from django.urls import path
from tests.views import get_questions, submit_responses, get_results

urlpatterns = [
    path("api/questions/", get_questions, name="get_questions"),
    path("api/submit/", submit_responses, name="submit_responses"),
    path("api/results/", get_results, name="get_results"),
]
