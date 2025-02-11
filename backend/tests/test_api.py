import uuid
import requests
from django.test import TestCase
from django.urls import reverse
from .models import Session, Question, Response

# ✅ API Base URL (Change when deploying to Render)
BASE_URL = "http://127.0.0.1:8000/api"

class APITestCase(TestCase):
    """✅ Unit tests for Django API"""

    def setUp(self):
        """🔧 Setup: Create a session and a question before running tests"""
        self.session = Session.objects.create(session_id=uuid.uuid4())
        self.question = Question.objects.create(text="Test Question?", order=1)

    def test_submit_responses(self):
        """✅ Test submitting valid responses"""
        url = reverse("submit_responses")
        data = {
            "session_id": str(self.session.session_id),
            "responses": [{"question_id": self.question.id, "answer_value": 5}]
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)  # ✅ Expecting success

    def test_duplicate_responses(self):
        """✅ Test submitting duplicate responses"""
        url = reverse("submit_responses")
        data = {
            "session_id": str(self.session.session_id),
            "responses": [{"question_id": self.question.id, "answer_value": 5}]
        }
        self.client.post(url, data, content_type="application/json")  # First submission
        response = self.client.post(url, data, content_type="application/json")  # Duplicate
        self.assertEqual(response.status_code, 400)  # ✅ Expecting error

    def test_get_results(self):
        """✅ Test retrieving valid results"""
        url = reverse("get_results") + f"?session_id={self.session.session_id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # ✅ Expecting success

    def test_invalid_submission(self):
        """✅ Test response submission with missing session_id & responses"""
        url = reverse("submit_responses")
        response = self.client.post(url, {}, content_type="application/json")
        self.assertEqual(response.json().get("error"), "Missing session_id or responses")

    def test_invalid_results_request(self):
        """✅ Test requesting results without session_id"""
        url = reverse("get_results")
        response = self.client.get(url)
        self.assertEqual(response.json().get("error"), "Missing session_id parameter")

    def test_invalid_uuid(self):
        """✅ Test API with an invalid session ID format"""
        url = reverse("get_results") + "?session_id=invalid_uuid"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "Invalid session ID format")

# ✅ External API Testing (Requests)
def test_api_root():
    response = requests.get(BASE_URL + "/")
    print("\n🌍 API Root:", response.status_code, response.text)

def test_submit_responses():
    data = {
        "session_id": "test-session-123",
        "responses": [{"question_id": 1, "answer_value": "A"}]
    }
    response = requests.post(BASE_URL + "/submit/", json=data)
    print("\n✅ Submit Responses:", response.status_code, response.json())

def test_get_results():
    params = {"session_id": "test-session-123"}
    response = requests.get(BASE_URL + "/results/", params=params)
    print("\n📊 Get Results:", response.status_code, response.json())

def test_invalid_submission():
    response = requests.post(BASE_URL + "/submit/", json={})
    print("\n❌ Invalid Submission:", response.status_code, response.json())

def test_invalid_results_request():
    response = requests.get(BASE_URL + "/results/")
    print("\n❌ Invalid Results Request:", response.status_code, response.json())

if __name__ == "__main__":
    test_api_root()
    test_submit_responses()
    test_get_results()
    test_invalid_submission()
    test_invalid_results_request()
