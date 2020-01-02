from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.core import serializers
from django.views.decorators.http import require_http_methods
import csv

from .forms import RegistrationForm, WorkoutForm
from.models import Workout, ExerciseType

def index(request):
    """
    Index View

    Loads the homepage.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = WorkoutForm(request.POST, request=request)
        
        # save form to create a new Workout
        if form.is_valid():
            form.save()

        # or re-render template with error message
        else:
            workouts = Workout.objects.select_related(
                "exercise_type").filter(user=request.user)

            data = []

            # parse DB results
            for workout in workouts:
                d = {
                    "date": workout.date.__str__(), 
                    "type": workout.exercise_type.name, 
                    "duration": workout.duration.__str__(), 
                    "distance": float(workout.distance)
                }
                data.append(d)

            context = {
                "form": form,
                "workouts": workouts,
                "data": data,
                "message": "Invalid Upload. Try Again"
            }

            return render(request, "workout_log/index.html", context)
    
    form = WorkoutForm()

    workouts = Workout.objects.select_related(
        "exercise_type").filter(user=request.user)

    # parse DB results 
    data = []
    for workout in workouts:
        d = {
            "date": workout.date.__str__(), 
            "type": workout.exercise_type.name, 
            "duration": workout.duration.__str__(), 
            "distance": float(workout.distance)
        }
        data.append(d)

    context = {
        "form": form,
        "workouts": workouts,
        "data": data
    }

    return render(request, "workout_log/index.html", context)


def login_view(request):
    """
    Login View

    Renders login page. If login for is submitted, the view authenticates the user,
    and logs them in if found, redirecting to the homepage. If not found, prints
    an 'Invalid Credentials' message an displays the login page.
    """
    if request.method == "POST":
        username = request.POST["username"]
        raw_password = request.POST["password"]
        user = authenticate(request, username=username, password=raw_password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "orders/workout_log.html",
                          {"message": "Invalid credentials"})

    return render(request, "workout_log/login.html")


def logout_view(request):
    """
    Logout View

    Logs the current user out, and redirects to the login page.
    """
    logout(request)
    return render(request, "workout_log/login.html", {"message": "Logged out"})


def register_view(request):
    """
    Registration View

    New user registration. This uses an extension of the built-in UserCreationForm
    called RegistrationForm to gather info such as first and last name, email, and
    2 passwords (identical) to validate the new user.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "workout_log/register.html", {"form": form})

    else:
        form = RegistrationForm()

        return render(request, "workout_log/register.html", {"form": form})

def export(request):
    """
    Export View

    Exports the user's workouts to csv
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    meta = Workout._meta

    field_names = [field.name for field in meta.fields]

    # open a csv writer
    response = HttpResponse(content_type="text/csv")
    response["ContentDisposition"] = "attachment; filename='results.csv'"
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    # write a new model instance on each row
    writer.writerow(field_names)
    for obj in Workout.objects.select_related("exercise_type").filter(user=request.user):
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


@require_http_methods(["POST"])
def update(request):
    """
    Update View

    Loads an updated dataset for visualization based on the ExerciseType selected.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # need a blonk form for rendering
    form = WorkoutForm()

    ex_type = request.POST.get("exercise-type")

    # load all workouts, or just one type
    if ex_type == "all":
        workouts = Workout.objects.select_related("exercise_type").filter(user=request.user)

    else:
        workouts = Workout.objects.select_related(
            "exercise_type").filter(user=request.user, exercise_type__name=ex_type)

    # parse DB results
    data = []
    for workout in workouts:
        d = {
            "date": workout.date.__str__(),
            "type": workout.exercise_type.name,
            "duration": workout.duration.__str__(),
            "distance": float(workout.distance)
        }
        data.append(d)

    context = {
        "form": form,
        "workouts": workouts,
        "data": data
    }

    return render(request, "workout_log/index.html", context)
