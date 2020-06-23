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


class WorkoutList(LoginRequiredMixin, View):
    # model = Workout
    login_url = 'account_login'

    def get(self, request):
        workouts = Workout.objects.filter(author=self.request.user)
        form = WorkoutCreateForm()
        context = {
            'form': form,
            'workouts': workouts,
            'workouts_len': len(workouts)
        }
        return render(request, 'diary/workout_list.html', context)


class ExerciseList(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, slug):
        workout = get_object_or_404(Workout, slug__iexact=slug, author=self.request.user)
        exercises = workout.exercise_mm.all()
        form = ExerciseCreateForm()
        context = {
            'workout': workout,
            'exercises': exercises,
            'exercises_len': len(exercises),
            'form': form,
        }
        return render(request, 'diary/exercise_list.html', context)


class E1xerciseDetail(View):
    def get(self, request, slug):
        form = SetCreateForm()
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        workout = get_object_or_404(Workout, slug=exercise.workout.slug)
        sets = exercise.set_mm.all()  # all sets in current exercise
        today_sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
        set_number = today_sets + 1
        # exact_set_date = sets.filter(date=date)

        # latest = sets.latest('date')  # latest set
        today = date.today()
        if sets:
            all_sets_count = len(sets)  # quantity of all sets
            all_dates = [set.date for set in sets]  # all sets dates
            all_dates = list(dict.fromkeys(all_dates))  # unique sets dates
            all_dates_count = len(all_dates)  # quantity of all unique dates
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
                last_dates = [all_dates[-2], all_dates[-1]]
            else:
                last_dates = [all_dates[0]]
            training_list_len = len(last_training_sets)

            volume = []
            weight_per_set = []
            for training in last_training_sets:
                training_day_volume = 0
                training_day_reps = 0
                for set in training:
                    if set.weight is not None:
                        set_volume = set.reps * set.weight
                        training_day_volume += set_volume
                        training_day_reps += set.reps
                    else:
                        set_volume = 0
                        training_day_volume += set_volume
                        training_day_reps += set.reps
                volume.append(training_day_volume)
                if training_day_volume:
                    if training_day_volume % training_day_reps == 0:
                        calc = round(training_day_volume / training_day_reps)
                        weight_per_set.append(calc)
                    else:
                        weight_per_set.append(round(training_day_volume / training_day_reps, 1))
                else:
                    training_day_reps = None
                    weight_per_set.append(training_day_reps)

            training_dict = {'sets': last_training_sets, 'dates': last_dates}
        else:
            last_training_sets = None
            all_dates = None
            all_sets_count = None
            all_dates_count = None
            all_dates_sets = None
            last_dates = None
            training_list_len = None
            last_sets_count = None
            volume = None
            weight_per_set = None

        context = {
            'form': form,
            'exercise': exercise,
            'set_list': sets,
            'all_dates': all_dates,
            'all_sets_count': all_sets_count,
            'all_dates_count': all_dates_count,
            'all_dates_sets': all_dates_sets,
            'today': today,
            'last_training_sets': last_training_sets,
            'last_dates': last_dates,
            'training_list_len': training_list_len,
            'last_sets_count': last_sets_count,
            'workout': workout,
            'set_number': set_number,
            'volume': volume,
            'weight_per_set': weight_per_set,
            # 'training_dict': training_dict,
        }
        return render(request, 'diary/exercise_detail.html', context)

    def post(self, request, slug):

        data = {}
        form = SetCreateForm(request.POST)
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        workout = get_object_or_404(Workout, slug=exercise.workout.slug)
        sets = exercise.set_mm.all()  # all sets in current exercise
        today_sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
        set_number = today_sets + 1
        new_form = SetCreateForm()
        today = date.today()
        if sets:
            all_dates = [set.date for set in sets]  # all sets dates
            all_dates = list(dict.fromkeys(all_dates))  # unique sets dates
            all_dates_count = len(all_dates)  # quantity of all unique dates
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
                last_dates = [all_dates[-2], all_dates[-1]]
            else:
                last_dates = [all_dates[0]]
            training_list_len = len(last_training_sets)

            volume = []
            weight_per_set = []
            for training in last_training_sets:
                training_day_volume = 0
                training_day_reps = 0
                for set in training:
                    if set.weight is not None:
                        set_volume = set.reps * set.weight
                        training_day_volume += set_volume
                        training_day_reps += set.reps
                    else:
                        set_volume = 0
                        training_day_volume += set_volume
                        training_day_reps += set.reps
                volume.append(training_day_volume)
                if training_day_volume:
                    if training_day_volume % training_day_reps == 0:
                        calc = round(training_day_volume / training_day_reps)
                        weight_per_set.append(calc)
                    else:
                        weight_per_set.append(round(training_day_volume / training_day_reps, 1))
                else:
                    training_day_reps = None
                    weight_per_set.append(training_day_reps)

            training_dict = {'sets': last_training_sets, 'dates': last_dates}

        else:
            last_training_sets = None
            all_dates = None
            all_dates_count = None
            all_dates_sets = None
            last_dates = None
            training_list_len = None
            last_sets_count = None
            volume = None
            weight_per_set = None

        context = {
            'exercise': exercise,
            'set_list': sets,
            'all_dates': all_dates,
            'all_dates_count': all_dates_count,
            'all_dates_sets': all_dates_sets,
            'today': today,
            'last_training_sets': last_training_sets,
            'last_dates': last_dates,
            'training_list_len': training_list_len,
            'last_sets_count': last_sets_count,
            'workout': workout,
            'set_number': set_number,
            'volume': volume,
            'weight_per_set': weight_per_set,
        }
        if form.is_valid():
            form = form.save(commit=False)
            form.set_number = set_number
            form.exercise = exercise
            form.author = self.request.user
            form.save()
            sets.append(form)
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/exercise_detail.html', context, request)
        else:
            data['form_is_valid'] = False


        return JsonResponse(data)


class SetList(View):
    def get(self, request, slug):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        today_sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
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
        return render(request, 'diary/set_list.html', context)

    def post(self, request, slug):
        data = {}
        form = SetCreateForm(request.POST)
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        today_sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
        set_number = today_sets + 1
        today = date.today()
        if form.is_valid():
            form = form.save(commit=False)
            form.set_number = set_number
            form.exercise = exercise
            form.author = self.request.user
            form.save()
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
            weight_per_rep = []
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
                volume.append(training_day_volume)
                if training_day_volume:
                    if training_day_volume % training_day_reps == 0:
                        calc = round(training_day_volume / training_day_reps)
                        weight_per_rep.append(calc)
                    else:
                        weight_per_rep.append(round(training_day_volume / training_day_reps, 1))
                else:
                    training_day_reps = None
                    weight_per_rep.append(training_day_reps)
            context = {
                'second_last_date': unique_dates[-2] if len(unique_dates) >= 2 else None,
                'last_date': unique_dates[-1] if unique_dates else None,
                'secondlast_sets': secondlast_sets,
                'last_sets': last_sets,
                'data': {
                    'secondlast_sets': {
                        'sets': secondlast_sets,
                        'date': unique_dates[-2] if len(unique_dates) >= 2 else None,
                        'volume': volume[-2] if len(volume) >= 2 else None,
                        'weight_per_rep': weight_per_rep[-2] if len(weight_per_rep) >= 2 else None,

                    },
                    'last_sets': {
                        'sets': last_sets,
                        'date': unique_dates[-1] if unique_dates else None,
                        'volume': volume[-1] if volume else None,
                        'weight_per_rep': weight_per_rep[-1] if weight_per_rep else None,
                    },
                },
                'exercise': exercise,
                'workout': workout,
                'volume': volume,
                'weight_per_rep': weight_per_rep,
            }
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/set_list.html', context, request)
        else:
            data['form_is_valid'] = False

        return JsonResponse(data)


class WorkoutCreateView(View):
    def post(self, request):
        data = {}
        form = WorkoutCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.save()
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/btn_group_workout.html', {
                'item': form,
            }, request)
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class WorkoutUpdateView(View):
    def post(self, request, slug):
        data = {}
        workout = Workout.objects.get(slug=slug)
        form = WorkoutCreateForm(request.POST, instance=workout)
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/btn_group_workout.html', {
                'item': workout,
                },
                request)
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class WorkoutDeleteView(View):
    def post(self, request, slug):
        data = {}
        workout = Workout.objects.get(slug=slug)
        workout.delete()
        data['deleted'] = True
        return JsonResponse(data)


class ExerciseCreateView(View):
    def post(self, request, slug):
        data = {}
        workout = Workout.objects.get(slug=slug)
        form = ExerciseCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.workout = workout
            form.author = self.request.user
            form.save()
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/btn_group_exercise.html', {
                'item': form,
            }, request)
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class SetCreateView(View):
    def post(self, request, slug):
        data = {}
        form = SetCreateForm(request.POST)
        exercise = Exercise.objects.get(slug=slug)
        sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
        set_number = sets + 1
        if form.is_valid():
            print(form.cleaned_data)
            form = form.save(commit=False)
            form.exercise = exercise
            form.author = self.request.user
            form.set_number = set_number
            form.save()
            data['form_is_valid'] = True
            print('============', form)
            data['html'] = render_to_string('diary/btn_group_set.html', {
                'item': form,
            }, request)
            print(data['html'])
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class SetUpdateView(View):
    def post(self, request, pk):
        data = {}
        set = Set.objects.get(pk=pk, author=self.request.user)
        form = SetCreateForm(request.POST, instance=set)
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/btn_group_set.html', {
                'item': set,
                },
                request)
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class SetDeleteView(View):
    def post(self, request, slug):
        data = {}
        set = Set.objects.get(pk=slug)
        sets = Set.objects.filter(author=self.request.user)
        set.delete()
        data['deleted'] = True
        data['html'] = render_to_string('diary/exercise_detail.html', {
            'workouts': workouts,
            'workouts_len': len(workouts),
            'workout': workout,
            },
            request)
        return JsonResponse(data)


class ExerciseDeleteView(View):
    def post(self, request, slug):
        data = {}
        exercise = Exercise.objects.get(slug=slug)
        exercise.delete()
        data['deleted'] = True
        return JsonResponse(data)


class ExerciseUpdateView(View):
    def post(self, request, slug):
        data = {}
        exercise = get_object_or_404(Exercise, slug__iexact=slug, author=self.request.user)
        form = ExerciseCreateForm(request.POST, instance=exercise)
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/btn_group_exercise.html', {
                'item': exercise,
                },
                request)
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class RegisterUserView(CreateView):
    model = User
    template_name = 'diary/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('workout_list_url')
    success_msg = 'User created'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class DiaryLoginView(LoginView):
    template_name = 'diary/login.html'
    form_class = AuthForm
    success_url = reverse_lazy('workout_list_url')

    def get_success_url(self):
        return self.success_url


class DiaryLogoutView(LogoutView):
    next_page = reverse_lazy('workout_list_url')