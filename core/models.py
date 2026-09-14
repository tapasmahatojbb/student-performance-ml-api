from django.db import models

# Create your models here.

class Student(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self):
        return self.name

class PredictionHistory(models.Model):

    study_hours = models.FloatField()
    attendance = models.FloatField()
    previous_marks = models.FloatField()

    prediction = models.CharField(
        max_length=10
    )

    probability = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.prediction} - {self.probability}%"
