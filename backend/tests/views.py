import json
import logging
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.views.decorators.http import require_http_methods

from .models import Question, Response, Session

# Configure logging for better debugging
logger = logging.getLogger(__name__)

# ✅ Full Scoring Keys - Ensure all 203 scales are included
SCORING_KEYS = {
    #✅ NEO PI-R Inventory
    "Anxiety": [1, 71, 162, 147, 33],  
    "Angry Hostility": [123, 33, 62, 24, 60],  
    "Depression": [57, 33, 160, 72, 1],  
    "Self-Consciousness": [72, 134, 49, 57, 30],  
    "Impulsiveness": [2, 126, 136, 165, 14],  
    "Vulnerability": [57, 162, 33, 72, 147],  
    "Warmth": [6, 170, 37, 166, 171],  
    "Gregariousness": [3, 73, 37, 135, 102],  
    "Assertiveness": [4, 101, 163, 145, 21],  
    "Activity": [5, 22, 31, 101, 163],  
    "Excitement-Seeking": [44, 46, 106, 79, 73],  
    "Positive Emotions": [6, 99, 123, 133, 37],  
    "Fantasy": [74, 138, 142, 115, 59],  
    "Aesthetics": [7, 75, 109, 26, 27],  
    "Feelings": [19, 85, 179, 150, 148],  
    "Actions": [42, 27, 94, 92, 138],  
    "Ideas": [110, 139, 161, 68, 100],  
    "Values": [76, 54, 59, 156, 98],  
    "Trust": [8, 123, 160, 166, 125],  
    "Straightforwardness": [9, 52, 86, 51, 46],  
    "Altruism": [10, 111, 123, 65, 166],  
    "Compliance": [104, 172, 178, 65, 34],  
    "Modesty": [11, 118, 120, 38, 176],  
    "Tender-Mindedness": [12, 77, 111, 114, 177],  
    "Competence": [167, 57, 116, 137, 101],  
    "Order": [13, 112, 90, 14, 137],  
    "Dutifulness": [151, 14, 45, 41, 116],  
    "Achievement Striving": [25, 14, 4, 48, 145],  
    "Self-Discipline": [14, 116, 152, 81, 167],  
    "Deliberation": [15, 35, 136, 41, 141],  

    # ✅ HEXACO-PI Inventory
    "Sincerity": [9, 78, 17, 86, 51],  
    "Fairness": [16, 46, 87, 104, 32],  
    "Greed Avoidance": [17, 97, 118, 78, 16],  
    "Fearfulness": [79, 105, 164, 162, 132],  
    "Social Boldness": [21, 30, 101, 163, 38],  
    "Sociability": [3, 37, 88, 170, 73],  
    "Liveliness": [22, 31, 6, 30, 99],  
    "Forgiveness": [114, 50, 34, 23, 121],  
    "Gentleness": [23, 24, 104, 40, 65],  
    "Patience": [24, 23, 62, 172, 104],  
    "Diligence": [25, 81, 48, 14, 116],  
    "Prudence": [41, 15, 141, 14, 167],  
    "Creativity": [84, 115, 138, 154, 68],  
    "Empathy": [19, 127, 10, 177, 77],  

    # ✅ JPI-R Inventory
    "Complexity": [139, 76, 43, 100, 59],  
    "Breadth of Interest": [27, 43, 75, 26, 83],  
    "Innovation": [138, 154, 84, 115, 110],  
    "Tolerance": [42, 34, 121, 50, 59],  
    "Cooperativeness": [29, 47, 95, 158, 162],  
    "Sociability": [3, 37, 135, 170, 113],  
    "Social Confidence": [30, 99, 101, 21, 88],  
    "Energy Level": [31, 22, 175, 152, 164],  
    "Risk Taking": [16, 79, 46, 61, 44],  
    "Traditional Values": [76, 54, 156, 104, 142],  

    # ✅ MPQ Inventory
    "Well-being": [117, 6, 22, 57, 160],  
    "Social Potency": [118, 38, 101, 4, 86],  
    "Achievement": [25, 110, 81, 137, 180],  
    "Social Closeness": [3, 37, 135, 170, 113],  
    "Stress Reaction": [33, 71, 1, 57, 49],  
    "Aggression": [34, 52, 119, 24, 16],  
    "Alienation": [49, 125, 57, 160, 180],  
    "Control": [35, 15, 141, 41, 167],  
    "Harm-avoidance": [79, 16, 132, 61, 35],  

    # ✅ TCI Inventory
    "Exploratory Excitability": [44, 94, 92, 42, 84],  
    "Impulsiveness": [35, 41, 15, 141, 131],  
    "Extravagance": [45, 155, 165, 169, 15],  
    "Worry & Pessimism": [1, 123, 71, 173, 57],  
    "Shyness with Strangers": [30, 88, 99, 37, 21],  
    "Fatigability": [31, 22, 175, 152, 167],  
    "Sentimentality": [19, 143, 80, 127, 166],  
    "Warm Communication": [37, 171, 88, 6, 85],  
    "Attachment": [85, 168, 171, 179, 20],  
    "Dependence": [47, 95, 70, 28, 158],  

    # ✅ CPI Inventory
    "Dominance": [21, 101, 4, 30, 163],  
    "Capacity for Status": [30, 21, 99, 38, 72],  
    "Sociability": [99, 30, 21, 37, 101],  
    "Social Presence": [99, 38, 30, 133, 72],  
    "Self-Acceptance": [21, 101, 30, 163, 99],  

    # ✅ HPI Inventory
    "Empathy": [62, 24, 173, 123, 23],  
    "Calmness": [33, 57, 162, 178, 148],  
    "Trusting": [8, 123, 125, 181, 60],  
    "Self-Confidence": [72, 57, 101, 134, 145],  
    "Leadership": [101, 4, 89, 118, 163],
}

@require_http_methods(["GET"])
def get_questions(request):
    """Retrieve all questions"""
    try:
        questions = list(Question.objects.values("id", "text"))
        return JsonResponse({"questions": questions})
    except Exception as e:
        logger.error(f"Error retrieving questions: {e}")
        return JsonResponse({"error": "Failed to fetch questions"}, status=500)


@require_http_methods(["GET"])
def get_question_by_id(request, question_id):
    """Retrieve a single question by ID"""
    try:
        question = Question.objects.get(id=question_id)
        return JsonResponse({"id": question.id, "text": question.text})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Question not found"}, status=404)
    except Exception as e:
        logger.error(f"Error retrieving question {question_id}: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt  # Required for API calls without CSRF tokens (e.g., frontend JavaScript)
@require_http_methods(["POST"])
def submit_responses(request):
    """Receive and save user responses"""
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        responses = data.get("responses", [])

        if not session_id or not responses:
            return JsonResponse({"error": "Missing session ID or responses"}, status=400)

        # Bulk insert for performance optimization
        response_objects = [
            Response(session_id=session_id, question_id=resp["question_id"], answer=resp["answer"])
            for resp in responses
        ]
        Response.objects.bulk_create(response_objects)

        return JsonResponse({"message": "Responses saved successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        logger.error(f"Error saving responses: {e}")
        return JsonResponse({"error": "Failed to save responses"}, status=500)


@require_http_methods(["GET"])
def get_results(request):
    """Compute user results based on responses"""
    try:
        session_id = request.GET.get("session_id")
        if not session_id:
            return JsonResponse({"error": "Session ID required"}, status=400)

        responses = Response.objects.filter(session_id=session_id).values("question_id", "answer")
        if not responses.exists():
            return JsonResponse({"error": "No responses found"}, status=404)

        # Compute scores based on SCORING_KEYS
        scores = {}
        for trait, question_ids in SCORING_KEYS.items():
            trait_responses = [resp["answer"] for resp in responses if resp["question_id"] in question_ids]
            if trait_responses:
                scores[trait] = round(np.mean(trait_responses), 2)

        return JsonResponse({"session_id": session_id, "scores": scores})

    except Exception as e:
        logger.error(f"Error computing results: {e}")
        return JsonResponse({"error": "Failed to compute results"}, status=500)


@require_http_methods(["DELETE"])
def delete_response(request, response_id):
    """Delete a specific response by ID (admin use)"""
    try:
        response = Response.objects.get(id=response_id)
        response.delete()
        return JsonResponse({"message": "Response deleted successfully"})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Response not found"}, status=404)
    except Exception as e:
        logger.error(f"Error deleting response {response_id}: {e}")
        return JsonResponse({"error": "Failed to delete response"}, status=500)

        from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question, Response

@csrf_exempt
def submit_responses(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            session_id = data.get("session_id")
            responses = data.get("responses")

            if not session_id or not responses:
                return JsonResponse({"error": "Missing session ID or responses"}, status=400)

            for response in responses:
                question_id = response.get("question_id")
                answer = response.get("answer")

                question = Question.objects.filter(id=question_id).first()
                if not question:
                    return JsonResponse({"error": "Invalid question ID"}, status=400)

                Response.objects.create(session_id=session_id, question=question, answer_value=answer)

            return JsonResponse({"message": "Responses submitted successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
