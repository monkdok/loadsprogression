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


class ExerciseDetail(View):
    def get(self, request, slug):
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        today_sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
        set_number = today_sets + 1
        today = date.today()
        workout = get_object_or_404(Workout, slug=exercise.workout.slug)
        all_sets = exercise.set_mm.filter(author=self.request.user)  # all sets in current exercise
        all_dates = [set.date for set in all_sets]  # all sets dates
        unique_dates = list(dict.fromkeys(all_dates))  # unique sets dates
        print('=========unique dates', sorted(unique_dates))
        last_sets = []
        secondlast_sets = []
        print('==========secondlast date', unique_dates[-2])
        print('==========last date', unique_dates[-1])
        if unique_dates:
            if len(unique_dates) >= 2:
                last_sets = [all_sets.filter(exercise=exercise, date=unique_dates[-1]).order_by('set_number')]
                secondlast_sets = [all_sets.filter(exercise=exercise, date=unique_dates[-2]).order_by('set_number')]
            else:
                last_sets = [all_sets.filter(exercise=exercise, date=unique_dates[-1]).order_by('set_number')]
                secondlast_sets = None
        context = {
            'second_last_date': unique_dates[-2] if len(unique_dates) >= 2 else None,
            'last_date': unique_dates[-1],
            'secondlast_sets': secondlast_sets,
            'last_sets': last_sets,
            'exercise': exercise,
            'workout': workout,

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
            print('=========unique dates', sorted(unique_dates))
            last_sets = []
            secondlast_sets = []
            print('==========secondlast date', unique_dates[-2])
            print('==========last date', unique_dates[-1])
            if unique_dates:
                if len(unique_dates) >= 2:
                    last_sets = [all_sets.filter(exercise=exercise, date=unique_dates[-1]).order_by('set_number')]
                    secondlast_sets = [all_sets.filter(exercise=exercise, date=unique_dates[-2]).order_by('set_number')]
                else:
                    last_sets = [all_sets.filter(exercise=exercise, date=unique_dates[-1]).order_by('set_number')]
                    secondlast_sets = None
            context = {
                'last_sets': last_sets,
                'secondlast_sets': secondlast_sets,
                'last_date': unique_dates[-1],
                'second_last_date': unique_dates[-2] if unique_dates >= 2 else None,

            }
            data['form_is_valid'] = True
            data['html'] = render_to_string('diary/exercise_detail.html', request)
        else:
            data['form_is_valid'] = False

        return JsonResponse(data)

# class ExerciseDetail(View):
#     def get(self, request, slug):
#         form = SetCreateForm()
#         exercise = get_object_or_404(Exercise, slug__iexact=slug)
#         workout1 = get_object_or_404(Workout, slug=exercise.workout.slug)
#         sets = exercise.set_mm.all()  # all sets in current exercise
#         today_sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
#         set_number = today_sets + 1
#         # exact_set_date = sets.filter(date=date)
#
#         # latest = sets.latest('date')  # latest set
#         today = date.today()
#         if sets:
#             all_sets_count = len(sets)  # quantity of all sets
#             all_dates = [set.date for set in sets]  # all sets dates
#             all_dates = list(dict.fromkeys(all_dates))  # unique sets dates
#             all_dates_count = len(all_dates)  # quantity of all unique dates
#             if all_dates_count >= 2:
#                 last_training_sets = [sets.filter(exercise=exercise, date=all_dates[-2]).order_by('set_number'),
#                                       sets.filter(exercise=exercise, date=all_dates[-1]).order_by('set_number')]
#                 if len(last_training_sets[0]) > len(last_training_sets[1]):
#                     last_sets_count = last_training_sets[0]
#                 else:
#                     last_sets_count = last_training_sets[1]
#
#             else:
#                 last_training_sets = [list(sets.filter(exercise=exercise, date=all_dates[0]).order_by('set_number'))]
#                 last_sets_count = last_training_sets[0]
#             all_dates_sets = [sets.filter(exercise=exercise, date=date) for date in all_dates]
#             if all_dates_count >= 2:
#                 last_dates = [all_dates[-2], all_dates[-1]]
#             else:
#                 last_dates = [all_dates[0]]
#             training_list_len = len(last_training_sets)
#
#             volume = []
#             weight_per_set = []
#             for training in last_training_sets:
#                 training_day_volume = 0
#                 training_day_reps = 0
#                 for set in training:
#                     if set.weight is not None:
#                         set_volume = set.reps * set.weight
#                         training_day_volume += set_volume
#                         training_day_reps += set.reps
#                     else:
#                         set_volume = 0
#                         training_day_volume += set_volume
#                         training_day_reps += set.reps
#                 volume.append(training_day_volume)
#                 if training_day_volume:
#                     if training_day_volume % training_day_reps == 0:
#                         calc = round(training_day_volume / training_day_reps)
#                         weight_per_set.append(calc)
#                     else:
#                         weight_per_set.append(round(training_day_volume / training_day_reps, 1))
#                 else:
#                     training_day_reps = None
#                     weight_per_set.append(training_day_reps)
#
#             training_dict = {'sets': last_training_sets, 'dates': last_dates}
#         else:
#             last_training_sets = None
#             all_dates = None
#             all_sets_count = None
#             all_dates_count = None
#             all_dates_sets = None
#             last_dates = None
#             training_list_len = None
#             last_sets_count = None
#             volume = None
#             weight_per_set = None
#
#         context = {
#             'form': form,
#             'exercise': exercise,
#             'set_list': sets,
#             'all_dates': all_dates,
#             'all_sets_count': all_sets_count,
#             'all_dates_count': all_dates_count,
#             'all_dates_sets': all_dates_sets,
#             'today': today,
#             'last_training_sets': last_training_sets,
#             'last_dates': last_dates,
#             'training_list_len': training_list_len,
#             'last_sets_count': last_sets_count,
#             'workout': workout1,
#             'set_number': set_number,
#             'volume': volume,
#             'weight_per_set': weight_per_set,
#             # 'training_dict': training_dict,
#         }
#         return render(request, 'diary/exercise_detail.html', context)
#
#     def post(self, request, slug, author, workout):
#         form = SetCreateForm(request.POST)
#         exercise = Exercise.objects.get(slug=slug)
#         sets = len(Set.objects.all().filter(exercise=exercise, date=date.today()))
#         set_number = sets + 1
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.set_number = set_number
#             form.exercise = exercise
#             form.author = self.request.user
#             # form.volume = form.weight * form.reps
#             form.save()
#
#         return HttpResponseRedirect(self.request.path_info)


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


class SetUpdateView(UpdateView):
    model = Set
    form_class = SetCreateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        view_name = 'exercise_detail_url'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={
            'slug': self.object.exercise.slug,
            'author': self.object.author,
            'workout': self.object.exercise.workout.slug,

        })


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