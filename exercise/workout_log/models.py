from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from math import floor

class ExerciseType(models.Model):
    '''
    Exercise Type Model

    This model lists the types of supported exercise for the training log, and
    is used to classify workout entries
    '''
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Workout(models.Model):
    '''
    Workout Model

    This model represents workout log entries for a user
    '''
    class Meta:
        ordering = ['date']
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name="workouts", blank=True, null=True)
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, 
        related_name="workouts")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    date = models.DateField(help_text="date of workout", default=date.today)

    # default distance is in miles
    distance = models.DecimalField(max_digits=5, decimal_places=2, 
        help_text="enter distance in miles (up to 2 decimal places)")

    # default duration is in minutes
    duration = models.DurationField(help_text="hh:mm:ss")
    
    def pace(self):
        pace = self.duration / self.distance
        return pace

    def speed(self):
        speed = self.distance / self.duration
        return speed
    
    def kilometers(self):
        return self.distance * 1.609

    def __str__(self):
        return f"{self.date} {self.exercise_type}, Distance: {self.distance} mi, Duration: {self.duration}"
