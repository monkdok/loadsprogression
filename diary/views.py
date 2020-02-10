from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingDay, Exercise, Set
from django.views.generic import View
# Create your views here.


def training_list(request):
    training = TrainingDay.objects.all()
    context = {'training': training}
    return render(request, 'diary/training_list.html', context)


class TrainingDetail(View):
    def get(self, request, slug):
        training = get_object_or_404(TrainingDay, slug__iexact=slug)
        context = {'training': training, 'exercises_list': training.exercises.all()}
        return render(request, 'diary/training_detail.html', context)


class ExerciseDetail(View):
    def get(self, request, slug):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        # список сетов
        sets = exercise.sets.all()
        context = {'exercise': exercise, 'sets_list': sets, 'set_date': date_list}
        return render(request, 'diary/exercise_detail.html', context)


