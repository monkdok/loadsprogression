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


class WorkoutList(LoginRequiredMixin, ObjectListMixin, View):
    login_url = 'account_login'
    model = Workout
    form = WorkoutCreateForm()
    template = 'diary/workout_list.html'


class ExerciseList(LoginRequiredMixin, ObjectListMixin, View):
    login_url = 'account_login'
    model = Workout
    template = 'diary/exercise_list.html'
    form = ExerciseCreateForm()

    def get_context_data(self, request, slug):
        context = super().get_context_data(request, slug)
        workout = get_object_or_404(Workout, slug__iexact=slug, author=self.request.user)
        exercises = workout.exercise_mm.all()
        context['workout'] = workout
        context['exercise'] = exercises
        context['exercises_len'] = len(exercises)
        return context


class SetList(SetListMixin, View):
    model = Set
    template = 'diary/set_list.html'


class WorkoutCreateView(ObjectCreateMixin, View):
    form = WorkoutCreateForm
    template = 'diary/btn_group_workout.html'


class WorkoutUpdateView(ObjectUpdateMixin, View):
    model = Workout
    form = WorkoutCreateForm
    template = 'diary/btn_group_workout.html'


class WorkoutDeleteView(View):
    def post(self, request, slug):
        data = {}
        workout = Workout.objects.get(slug=slug)
        workout.delete()
        data['deleted'] = True
        return JsonResponse(data)


class ExerciseCreateView(ObjectCreateMixin, View):
    form = ExerciseCreateForm
    template = 'diary/btn_group_exercise.html'
    parent = Workout


class SetCreateView(View):
    form = SetCreateForm
    template = 'diary/btn_group_set.html'
    parent = Exercise


class SetUpdateView(ObjectUpdateMixin, View):
    model = Set
    form = SetCreateForm
    template = 'diary/set_list.html'


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


class ExerciseUpdateView(ObjectUpdateMixin, View):
    model = Exercise
    form = ExerciseCreateForm
    template = 'diary/btn_group_exercise.html'


class ExerciseDeleteView(View):
    def post(self, request, slug):
        data = {}
        exercise = Exercise.objects.get(slug=slug)
        exercise.delete()
        data['deleted'] = True
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