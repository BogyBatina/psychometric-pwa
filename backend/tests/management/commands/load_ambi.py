from django.core.management.base import BaseCommand
from tests.models import Question

QUESTIONS = [
    "Rarely worry.",
    "Often eat too much.",
    "Usually like to spend my free time with people.",
    "Take charge.",
    "Am always busy.",
    "Radiate joy.",
    "Do not like poetry.",
    "Distrust people.",
    "Tell other people what they want to hear so that they will do what I want them to do.",
    "Anticipate the needs of others.",
    "Believe that I am better than others.",
    "Sympathize with the homeless.",
    "Keep things tidy.",
    "Am a highly disciplined person.",
    "Jump into things without thinking.",
    "Admire a really clever scam.",
    "Like to own things that impress people.",
    "Try to be with someone else when I'm feeling badly.",
    "Feel others’ emotions.",
    "Talk a lot.",
    "Try to avoid speaking in public.",
    "Am usually active and full of energy.",
    "Am patient with people who annoy me.",
    "Am easily annoyed.",
    "Push myself very hard to succeed.",
    "Do not like art.",
    "Love to hear about other countries and cultures.",
    "Am considered to be kind of eccentric.",
    "Worry about what people think of me.",
    "Am very shy in social situations.",
    "Don't have much energy.",
    "Don't think that laws apply to me.",
    "Have frequent mood swings.",
    "Hold a grudge.",
    "Like to act on a whim.",
    "Have felt the presence of another person when he or she was not really there.",
    "Seem to derive less enjoyment from interacting with people than others do.",
    "Love to be the center of attention.",
    "Don't let others cut in front of me in line.",
    "Insist that others do things my way.",
    "Am a firm believer in thinking things through.",
    "Dislike changes.",
    "Read a large variety of books.",
    "Love excitement.",
    "Would rather spend money than save it.",
    "Enjoy being reckless.",
    "Have never cared much what others thought of me.",
    "Usually get right to work on something that needs to be done as soon as I think of it.",
    "Often have the feeling that others laugh or talk about me.",
    "Try to forgive and forget.",
    "Feel little concern for others.",
    # Continue with all 181 questions...
]

class Command(BaseCommand):
    help = "Load AMBI test questions into the database."

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        for i, q in enumerate(QUESTIONS, start=1):
            Question.objects.create(text=q, order=i)
        self.stdout.write(self.style.SUCCESS("Successfully loaded AMBI questions."))
