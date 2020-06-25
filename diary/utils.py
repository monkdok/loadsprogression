from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from datetime import date
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, ListView, DeleteView, UpdateView, TemplateView, DetailView, CreateView
from .forms import *
import datetime


class SetListMixin(object):
    model = Set
    template = 'diary/set_list.html'

    def get_context_data(self, request, slug):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        today_sets = len(self.model.objects.all().filter(exercise=exercise, date=date.today()))
        set_number = today_sets + 1
        today = date.today()
        workout = get_object_or_404(Workout, slug=exercise.workout.slug)
        all_sets = exercise.set_mm.filter(author=self.request.user)  # all sets in current exercise
        all_dates = [set.date for set in all_sets]  # all sets dates
        unique_dates = list(dict.fromkeys(all_dates))  # unique sets dates
        last_sets = []
        secondlast_sets = []
        if unique_dates:

            if len(unique_dates) >= 2:
                last_sets = all_sets.filter(exercise=exercise, date=unique_dates[-1]).order_by('set_number')
                secondlast_sets = all_sets.filter(exercise=exercise, date=unique_dates[-2]).order_by('set_number')
            else:
                last_sets = all_sets.filter(exercise=exercise, date=unique_dates[-1]).order_by('set_number')
                secondlast_sets = []

        # volume calculating
        both_sets = [secondlast_sets, last_sets]
        volume = []
        average_weight = []
        average_reps = []
        for training in both_sets:
            training_day_volume = 0
            training_day_reps = 0
            for set in training:
                if set.weight is not None:
                    training_day_volume += set.volume
                    training_day_reps += set.reps
                else:
                    set_volume = 0
                    training_day_volume += set_volume
                    training_day_reps += set.reps
            if training_day_reps:
                average_reps.append(int(training_day_reps / len(training)))
            volume.append(training_day_volume)
            if training_day_volume:
                if training_day_volume % training_day_reps == 0:
                    calc = round(training_day_volume / training_day_reps)
                    average_weight.append(int(calc))
                else:
                    calc = round(training_day_volume / training_day_reps, 1)
                    average_weight.append(int(calc))
            else:
                training_day_reps = None
                average_weight.append(training_day_reps)

        context = {
            'set_number': set_number,
            'second_last_date': unique_dates[-2] if len(unique_dates) >= 2 else None,
            'last_date': unique_dates[-1] if unique_dates else None,
            'secondlast_sets': secondlast_sets,
            'last_sets': last_sets,
            'data': {
                'secondlast_sets': {
                    'sets': secondlast_sets,
                    'date': unique_dates[-2] if len(unique_dates) >= 2 else None,
                    'volume': volume[-2] if len(volume) >= 2 else None,
                    'average_weight': average_weight[-2] if len(average_weight) >= 2 else None,

                },
                'last_sets': {
                    'sets': last_sets,
                    'date': unique_dates[-1] if unique_dates else None,
                    'volume': volume[-1] if volume else None,
                    'average_weight': average_weight[-1] if average_weight else None,
                },
            },
            'exercise': exercise,
            'workout': workout,
            'volume': volume,
            'average_weight': average_weight,
            'average_reps': average_reps,
            'average_set': {
                'secondlast_average_set': {
                    'weight': average_weight[-2] if len(average_weight) >= 2 else None,
                    'reps': average_reps[-2] if len(average_reps) >= 2 else None,
                },
                'last_average_set': {
                    'weight': average_weight[-1] if average_weight else None,
                    'reps': average_reps[-1] if average_reps else None,
                }
            }
        }
        return context

    def get(self, request, slug):
        context = self.get_context_data(request, slug)
        return render(request, 'diary/set_list.html', context)

    def post(self, request, slug):
        data = {}
        form = SetCreateForm(request.POST)
        context = self.get_context_data(request, slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.set_number = context['set_number']
            form.exercise = context['exercise']
            form.author = self.request.user
            form.save()
            context = self.get_context_data(request, slug)
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/set_list.html', context, request)
        else:
            data['form_is_valid'] = False

        return JsonResponse(data)
