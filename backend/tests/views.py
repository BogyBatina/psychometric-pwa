from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
import numpy as np
import json

from tests.models import Question, Response, Session

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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json

from tests.models import Question, Response, Session

# ✅ Get all questions (handles errors)
def get_questions(request):
    try:
        questions = list(Question.objects.all().order_by("id").values("id", "text"))
        return JsonResponse({"questions": questions}, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Failed to fetch questions: {str(e)}"}, status=500)

# ✅ Submit responses (handles errors)
@csrf_exempt
def submit_responses(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        responses = data.get("responses")

        if not session_id or not isinstance(responses, list):
            return JsonResponse({"error": "Invalid data format"}, status=400)

        session, _ = Session.objects.get_or_create(session_id=session_id)

        for response in responses:
            question_id = response.get("question_id")
            score = response.get("score")

            if not question_id or score is None:
                continue

            question = Question.objects.get(id=question_id)
            Response.objects.update_or_create(session=session, question=question, defaults={"score": score})

        return JsonResponse({"message": "Responses saved successfully"})

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Invalid question ID"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ✅ Get results (handles errors)
@csrf_exempt
def get_results(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")

        if not session_id:
            return JsonResponse({"error": "Missing session_id"}, status=400)

        percentiles = calculate_scores(session_id)

        return JsonResponse({"percentiles": percentiles})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)