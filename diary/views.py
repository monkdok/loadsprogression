from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from datetime import date


from .models import Exercise, Set, Workout
from django.views.generic import View, ListView, DeleteView, TemplateView, DetailView
from .forms import *
from django.views.generic.dates import ArchiveIndexView

# Create your views here.


class WorkoutList(ListView):
    model = Workout
    # template_name = 'diary/workout_list.html'


# def workout_list(request):
#     workouts = Workout.objects.all()
#     context = {'workout_list': workouts}
#     return render(request, 'diary/workout_list.html', context)


# class ExerciseList(ListView):
#     model = Exercise
#     # template_name = 'diary/exercise_list.html'
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         workout = Workout.objects.get(slug__iexact=slug)
#         context['workout'] = workout
#         context['exercise_list'] = workout.exercise_mm.all()
#         return context


class WorkoutDetail(View):
    def get(self, request, slug):
        workout = get_object_or_404(Workout, slug__iexact=slug)
        # context = {'workout': workout, 'exercises_list': workout.exercises.all()}
        exercises = workout.exercise_mm.all()
        context = {
            'workout': workout,
            'exercises_list': exercises
        }
        return render(request, 'diary/exercise_list.html', context)


class ExerciseDetail(View):
    def get(self, request, slug, date_set=None):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        sets = exercise.set_mm.all()  # all sets in current exercise
        # exact_set_date = sets.filter(date=date)
        all_sets_count = len(sets)  # quantity of all sets
        all_dates = [set.date for set in sets]  # all sets dates
        all_dates = list(dict.fromkeys(all_dates))  # unique sets dates
        all_dates_count = len(all_dates)  # quantity of all unique dates
        latest = sets.latest('date')  # latest set
        today = date.today()
        if all_dates_count >= 2:
            last_training_sets = [sets.filter(exercise=exercise, date=all_dates[-2]).order_by('set_number'),
                                  sets.filter(exercise=exercise, date=all_dates[-1]).order_by('set_number')]
            if len(last_training_sets[0]) > len(last_training_sets[1]):
                last_sets_count = last_training_sets[0]
            else:
                last_sets_count = last_training_sets[1]

        else:
            last_training_sets = [list(sets.filter(exercise=exercise, date=all_dates[0]).order_by('set_number'))]
            last_sets_count = last_training_sets[0]
        all_dates_sets = [sets.filter(exercise=exercise, date=date) for date in all_dates]
        if all_dates_count >= 2:
            last_date = [all_dates[-2], all_dates[-1]]
        else:
            last_date = [all_dates[0]]
        training_list_len = len(last_training_sets)

        context = {
            'exercise': exercise,
            'set_list': sets,
            'all_dates': all_dates,
            'all_sets_count': all_sets_count,
            'latest': latest,
            'all_dates_count': all_dates_count,
            'all_dates_sets': all_dates_sets,
            'today': today,
            'last_training_sets': last_training_sets,
            'last_date': last_date,
            'training_list_len': training_list_len,
            'last_sets_count': last_sets_count,
        }
        return render(request, 'diary/exercise_detail.html', context)


# class ExerciseArchiveDetail:
#     def get(self, request, slug, date):


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
    success_url = reverse_lazy('workout_list_url')


