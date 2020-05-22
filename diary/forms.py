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
               # 'description',
          ]

          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'workout name'}),
               # 'description': forms.Textarea(attrs={'class': 'form-control'}),
               }

     def get_absolute_url(self):
          return reverse('workout_create_url')


class ExerciseCreateForm(forms.ModelForm):
     class Meta:
          model = Exercise
          fields = [
               'title',
               # 'description',
          ]

          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'exercise name'}),
               # 'description': forms.Textarea(attrs={'class': 'form-control'}),
               }


class SetCreateForm(forms.ModelForm):
     class Meta:
          model = Set
          fields = [
               'weight',
               'reps',
               'rest_time',
               ]

          widgets = {
               'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'weight'}),
               'reps': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'repetitions'}),
               'rest_time': forms.HiddenInput(),
               }


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

