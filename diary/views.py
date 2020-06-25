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
from .utils import *
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


class SetList(SetListMixin, View):
    model = Set
    template = 'diary/set_list.html'


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