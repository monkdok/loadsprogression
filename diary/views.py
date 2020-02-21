from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Exercise, Set, Workout
from django.views.generic import View, ListView, DeleteView
from .forms import *
from django.views.generic.dates import ArchiveIndexView

# Create your views here.


def workout_list(request):
    workouts = Workout.objects.all()
    context = {'workout_list': workouts}
    return render(request, 'diary/workout_list.html', context)


class WorkoutDetail(View):
    def get(self, request, slug):
        workout = get_object_or_404(Workout, slug__iexact=slug)
        # context = {'workout': workout, 'exercises_list': workout.exercises.all()}
        exercises = workout.exercise_mm.all()
        context = {
            'workout': workout,
            'exercises_list': exercises
        }
        return render(request, 'diary/workout_detail.html', context)


class ExerciseDetail(View):
    def get(self, request, slug):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        sets = exercise.set_mm.all()
        sets_count = len(sets)
        # all sets date
        all_dates = []
        for set in sets:
            all_dates.append(set.date)
        all_dates = list(dict.fromkeys(all_dates))
        all_dates_count = len(all_dates)
        latest = Set.objects.latest('date')
        # sets_by_date = Set.objects.filter(exercise=exercise, date=latest.date).order_by('set_number')
        if sets:
            sets_by_date = Set.objects.filter(exercise=exercise, date=all_dates[-1]).order_by('set_number')
        else:
            sets_by_date = None
        all_dates_sets = []
        for date in all_dates:
            sets = list(Set.objects.filter(exercise=exercise, date=date))
        context = {
            'exercise': exercise,
            'set_list': sets,
            'all_dates': all_dates,
            'sets_count': sets_count,
            'latest': latest,
            'all_dates_count': all_dates_count,
            'sets_by_date': sets_by_date,
            'all_dates_sets': all_dates_sets
        }
        return render(request, 'diary/exercise_detail.html', context)


def workout_create_view(request):
    form = WorkoutCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = WorkoutCreateForm()
    context = {
        'form': form
    }
    return render(request, 'diary/workout_create.html', context)


def exercise_create_view(request):
    form = ExerciseCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ExerciseCreateForm()
    context = {
        'form': form
    }
    return render(request, 'diary/exercise_create.html', context)


def set_create_view(request):
    form = SetCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('../')
    context = {
        'form': form
    }
    return render(request, 'diary/set_create.html', context)


# def set_delete_view(request, id):
#     obj = get_object_or_404(Set, id=id)
#     if request.method == 'POST':
#         obj.delete()
#         return redirect('../')
#     context = {
#         'obj': obj
#     }
#     return render(request, 'diary/set_delete.html', context)

class SetDeleteView(DeleteView):
    model = Set
    template_name = 'diary/set_delete.html'
    success_url = reverse_lazy('./')


