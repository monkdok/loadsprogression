from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingDay, Exercise, Set, Category
from django.views.generic import View
# Create your views here.


def training_list(request):
    training = Category.objects.all()
    context = {'training_list': training}
    return render(request, 'diary/training_list.html', context)


class CategoryDetail(View):
    def get(self, request, slug):
        training = get_object_or_404(Category, slug__iexact=slug)
        context = {'training': training, 'exercises_list': training.exercises.all()}
        return render(request, 'diary/training_detail.html', context)


class ExerciseDetail(View):
    def get(self, request, slug):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        context = {'exercise': exercise}
        return render(request, 'diary/exercise_detail.html', context)


