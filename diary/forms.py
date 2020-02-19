from django import forms
from .models import *
from django.core.exceptions import ValidationError


class WorkoutCreateForm(forms.ModelForm):
     class Meta:
          model = Workout
          fields = [
               'title',
               'description',
          ]

     def get_absolute_url(self):
          return reverse('workout_create_url')


class ExerciseCreateForm(forms.ModelForm):
     class Meta:
          model = Exercise
          fields = [
               'title',
               'description',
               'workout',
          ]

     # def get_absolute_url(self):
     #      return reverse('workout_create_url')
