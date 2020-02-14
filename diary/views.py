from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Set, Workout
from django.views.generic import View
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
        context = {'workout': workout, 'exercises_list': exercises}
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
        latest = Set.objects.order_by('date')
        # exact_date_sets = list(Set.objects.filter(date=all_dates[0]))
        context = {'exercise': exercise, 'set_list': sets, 'all_dates': all_dates, 'sets_count': sets_count,
                   'latest': latest, 'all_dates_count': all_dates_count}
        return render(request, 'diary/exercise_detail.html', context)

