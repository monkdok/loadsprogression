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
from django.urls import path
from .views import *
from django.views.generic.dates import ArchiveIndexView

urlpatterns = [
    path('', workout_list, name='workout_list_url'),
    path('workout/<str:slug>/', WorkoutDetail.as_view(), name='workout_detail_url'),
    path('workout_create/', workout_create_view, name='workout_create_url'),
    path('exercise/<str:slug>/', ExerciseDetail.as_view(), name='exercise_detail_url'),
    path('exercise_create/', exercise_create_view, name='exercise_create_url'),
    path('set_create/', set_create_view, name='set_create_url'),
    path('set_delete/', set_delete_view, name='set_delete_url'),
    path('<str:exercise>/archive/<str:slug>/', WorkoutDetail.as_view(), name='sets_archive_url'),
    # path('archive/', ArchiveIndexView.as_view(model=Set, date_field="date"), name="set_archive"),
]
