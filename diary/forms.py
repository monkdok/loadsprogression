from django import forms
from django.contrib.auth.models import User

from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class WorkoutCreateForm(forms.ModelForm):
     class Meta:
          model = Workout
          fields = [
               'title',
               'description',
          ]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'


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

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'


class SetCreateForm(forms.ModelForm):
     class Meta:
          model = Set
          fields = [
               'set_number',
               'weight',
               'reps',
               'exercise',
          ]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'

class AuthForm(AuthenticationForm, forms.ModelForm):
     class Meta:
          model = User
          fields = [
               'username',
               'password',
          ]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):
     class Meta:
          model = User
          fields = [
               'username',
               'password',
          ]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'

     def save(self, commit=True):
          user = super().save(commit=False)
          user.set_password(self.cleaned_data["password"])
          if commit:
               user.save()
          return user

