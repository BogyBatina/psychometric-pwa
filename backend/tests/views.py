SCORING_KEYS = {
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
    "Emotional Stability": [1, 71, 33, 162, 147],
    "Honesty": [9, 78, 17, 86, 51],
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
    "Work Orientation": [33, 57, 160, 165, 159],
    "Traditionalism": [76, 54, 61, 59, 100],
    "Achievement": [25, 110, 81, 137, 180],
    "Self-Control": [35, 93, 142, 44, 94],
    "Harm Avoidance": [79, 16, 132, 61, 35],
    "Novelty Seeking": [44, 94, 92, 42, 84],
    "Spiritual Acceptance": [53, 156, 54, 114, 6],
    "Leadership": [101, 4, 89, 118, 163],
    "Skepticism": [8, 123, 125, 181, 60],
}

from django.db.models import Avg
import numpy as np

def calculate_scores(session_id):
    session = Session.objects.get(session_id=session_id)
    responses = Response.objects.filter(session=session)

    scores = {}

    for scale, questions in SCORING_KEYS.items():
        scale_score = 0
        for q_id in questions:
            response = responses.get(question_id=q_id)
            if response.question.reverse_scored:
                scale_score += (6 - response.score)  # Reverse scoring
            else:
                scale_score += response.score

        scores[scale] = scale_score

    # Convert raw scores into percentiles
    all_scores = list(scores.values())
    mean = np.mean(all_scores)
    std_dev = np.std(all_scores)

    percentiles = {scale: int((score - mean) / std_dev * 100) for scale, score in scores.items()}

    return percentiles

@csrf_exempt
def get_results(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")
        percentiles = calculate_scores(session_id)
        return JsonResponse({"percentiles": percentiles})

    return JsonResponse({"error": "Invalid request"}, status=400)
