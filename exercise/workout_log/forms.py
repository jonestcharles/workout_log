from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Workout

class RegistrationForm(UserCreationForm):
    """
    Class RegistrationForm

    Extends UserCreationForm. Adds form fields for first and last name, as well
    as email.
    """
    first_name = forms.CharField(
        max_length=30, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise_type', 'date', 'distance', 'duration']

    def __init__(self, *args, **kwargs):
       self.request = kwargs.pop('request', None)
       super(WorkoutForm, self).__init__(*args, **kwargs)


    def save(self, *args, **kwargs):
        kwargs['commit']=False
        obj = super(WorkoutForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request.user
        obj.save()
        return obj
