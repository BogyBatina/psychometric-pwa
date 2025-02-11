from django.db import models
import uuid

class Session(models.Model):
    """Stores unique test session identifiers."""
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} (Created: {self.created_at})"


class Question(models.Model):
    """Represents a psychometric test question."""
    text = models.TextField(null=False, blank=False)
    order = models.PositiveIntegerField(default=0)  # Ensuring valid order values

    class Meta:
        ordering = ["order"]  # Ensures questions are returned in order

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}"  # Display first 50 chars


class Response(models.Model):
    """Stores a user's response to a specific question."""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    answer_value = models.PositiveSmallIntegerField()  # Ensures valid integer range

    class Meta:
        unique_together = ("session", "question")  # Prevents duplicate responses

    def __str__(self):
        return f"Session {self.session.session_id} - Q{self.question.order}: {self.answer_value}"
