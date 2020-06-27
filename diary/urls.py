"""loadsprogression URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from .views import *
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import TemplateView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', WorkoutList.as_view(), name='workout_list_url'),
    path('workout/<str:slug>/', ExerciseList.as_view(), name='exercise_list'),
    path('workout/<str:slug>/update/', WorkoutUpdateView.as_view(), name='workout_update_view'),
    path('exercise/<str:slug>/', SetList.as_view(), name='exercise_detail_url'),
    path('exercise/<str:slug>/update', ExerciseUpdateView.as_view(), name='exercise_update_view'),
    path('set/<int:pk>/update', SetUpdateView.as_view(), name='set_update_view'),
    path('workout_create/', WorkoutCreateView.as_view(), name='workout_create_url'),
    path('workout/<str:slug>/exercise_create/', ExerciseCreateView.as_view(), name='exercise_create_url'),
    path('<str:slug>/set_create/', SetCreateView.as_view(), name='set_create_url'),
    path('set/<int:pk>/set_delete', SetDeleteView.as_view(), name='set_delete_url'),
    path('exercise/<str:slug>/exercise_delete', ExerciseDeleteView.as_view(), name='exercise_delete_url'),
    path('exercise/delete/<int:pk>/', ExerciseDeleteView.as_view(), name='exercise_delete_url'),
    path('workout/<str:slug>/workout_delete', WorkoutDeleteView.as_view(), name='workout_delete_url'),

]

urlpatterns += staticfiles_urlpatterns()