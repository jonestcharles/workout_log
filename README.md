# workout_log
A workout log powered by Django, using D# j for data viz

The app workout_log in exercise is a platform that allows users to upload run,
swim, or bike workouts and see them visualized on a graph. This uses Django and
D3 for data visualization.

1. Login/Logout/Register

This app uses Django's native authentication features to logn and register users.
All users who are not logged in are redirected to login for authentication. A
custom form, RegistrationFrom in forms.py, extends UserCreationForm and adds fields
to the register view (see views.py). This form automatically creates a new user,
who is then authenticated by the view.

2. Admin Dashboard

Both models (see belwo) are registered with custom ModelAdmin classes in admin.py
which displays more data fields n the list view on the admin dashboard.

3. Data Models.

In models.py, 2 models are defined. ExerciseType only consists of a name, in this
case Run, Swim, or Bike. Users cannot add ExerciseTypes. Workouts are instances of
a workout. Each Workout has a user, an ExerciseType, a date, a created and updated
timestamp, and a distance and duration. Each model instance also has methods for
their pace and speed, as well as converting the distance field (in miles) to km.
Currently, speed and pace are not used in the app, due to difficulty implementing
D3.

4. index.html

Once authenticated,the user is brought to the index page, where they see a list
of all their workouts. Their workouts are also visualized using D3.js. They see
a stacked bar graph of their wokrouts by day, color coded by type. The D# js script
is found in index.py, and runs each time the tempalte is rendered.

5. Display Update

A user can select a workout type from the dropdown menu. When submitted, this
refreshes the data to only workouts of that type. This is done in views.py, using
the exercise type as a flag to filter a DB query.

6. CSV Download

A user can also download all their workouts to a csv file. This is accomplished in
views.py (export view). A csv writer from Python's csv library writes a csv file
to an HttpResonse where each line is the fields from a Workout instance.

7. Workout Submit

A user can submit a new Workout using the form in index.html. This uses a custom
form defined in forms.py by extending the ModelForm class. WorkoutForm is tied
to the Workout model, and creates fields for all forms except user, which is
populated in a custome save() method, called in views.py, and the created and 
updated timestamps, which default to the current time on creation or update.
