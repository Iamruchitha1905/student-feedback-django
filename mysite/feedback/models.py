from django.db import models

class Feedback(models.Model):
    COURSE_CHOICES = [
        ("Python", "Python"),
        ("Django", "Django"),
        ("Java", "Java"),
        ("C++", "C++"),
        ("Data Science", "Data Science"),
    ]

    RATING_CHOICES = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course}"