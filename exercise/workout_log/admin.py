from django.contrib import admin
from .models import ExerciseType, Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """
    Register Workout with a custom view
    """
    list_display = ("user", "date", "exercise_type", "distance", "duration")

@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    """
    Register ExerciseType with a custom view
    """
    list_display = ("name", "pk")
    