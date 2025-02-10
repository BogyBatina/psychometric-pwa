from django.db import models
import uuid

class Session(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    text = models.TextField()
    order = models.PositiveIntegerField()
    reverse_scored = models.BooleanField(default=False)  # Flag for reverse-scoring

    def __str__(self):
        return f"{self.order}: {self.text}"

class Response(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()  # User response (1-5)
