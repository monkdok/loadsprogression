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

urlpatterns = [
    path('', training_list, name='training_list_url'),
    path('training/<str:slug>/', CategoryDetail.as_view(), name='category_detail_url'),
    path('exercise/<str:slug>/', ExerciseDetail.as_view(), name='exercise_detail_url'),
    # path('<str:slug>', exercise_list, name='exercise_list_url'),
    # path('<str:slug>', exercise_detail, name='exercise_detail_url'),

]
