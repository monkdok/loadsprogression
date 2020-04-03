from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from datetime import date
from django.contrib.auth.views import LoginView, LogoutView


from .models import Exercise, Set, Workout
from django.views.generic import View, ListView, DeleteView, UpdateView, TemplateView, DetailView, CreateView
from .forms import *
from django.views.generic.dates import ArchiveIndexView


class WorkoutList(LoginRequiredMixin, View):
    # model = Workout
    login_url = 'account_login'

    def get(self, request):
        workouts = Workout.objects.filter(author=self.request.user)
        form = WorkoutCreateForm()
        context = {
            'form': form,
            'workouts': workouts,
        }
        return render(request, 'diary/workout_list.html', context)

    def post(self, request):
        form = WorkoutCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.save()
        return HttpResponseRedirect(self.request.path_info)

    # def get_queryset(self):
    #     return super(WorkoutList, self).get_queryset().filter(author=self.request.user)


class WorkoutDetail(View):
    def get(self, request, slug):
        workout = get_object_or_404(Workout, slug__iexact=slug)
        exercises = workout.exercise_mm.all()
        form = ExerciseCreateForm()

        context = {
            'workout': workout,
            'exercises_list': exercises,
            'form': form,
        }
        return render(request, 'diary/exercise_list.html', context)

    def post(self, request, slug):
        form = ExerciseCreateForm(request.POST)
        workout = Workout.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.workout = workout
            form.save()
        return HttpResponseRedirect(self.request.path_info)


class ExerciseDetail(View):
    def get(self, request, slug, author, workout):
        form = SetCreateForm()
        exercise = get_object_or_404(Exercise, slug__iexact=slug)
        workout = workout
        workout1 = get_object_or_404(Workout, slug=exercise.workout.slug)
        sets = exercise.set_mm.all()  # all sets in current exercise
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
                last_date = [all_dates[-2], all_dates[-1]]
            else:
                last_date = [all_dates[0]]
            training_list_len = len(last_training_sets)
        else:
            last_training_sets = None
            all_dates = None
            all_sets_count = None
            all_dates_count = None
            all_dates_sets = None
            last_date = None
            training_list_len = None
            last_sets_count = None

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
            'last_date': last_date,
            'training_list_len': training_list_len,
            'last_sets_count': last_sets_count,
            'workout': workout1,
        }
        return render(request, 'diary/exercise_detail.html', context)

    def post(self, request, slug, author, workout):
        form = SetCreateForm(request.POST)
        exercise = Exercise.objects.get(slug=slug)
        sets = len(Set.objects.all().filter(exercise=exercise))
        set_number = sets + 1
        if form.is_valid():
            form = form.save(commit=False)
            form.set_number = set_number
            form.exercise = exercise
            form.author = self.request.user
            form.save()

        return HttpResponseRedirect(self.request.path_info)


class WorkoutCreateView(View):
    def get(self, request):
        form = WorkoutCreateForm()
        return render(request, 'diary/workout_form.html', {'form': form})

    def post(self, request):
        form = WorkoutCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.save()
        return redirect('workout_list_url')


class ExerciseCreateView(View):
    def get(self, request, slug):
        form = ExerciseCreateForm()
        return render(request, 'diary/exercise_form.html', {'form': form})

    def post(self, request, slug):
        form = ExerciseCreateForm(request.POST)
        workout = Workout.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.workout = workout
            form.author = self.request.user
            form.save()
        return redirect('workout_list_url')


class SetCreateView(View):
    def get(self, request, slug):
        form = SetCreateForm()
        return render(request, 'diary/set_form.html', {'form': form})

    def post(self, request, slug):
        form = SetCreateForm(request.POST)
        exercise = Exercise.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.exercise = exercise
            form.author = self.request.user
            form.save()
        return redirect('workout_list_url')


class SetDeleteView(DeleteView):
    model = Set
    template_name = 'diary/set_delete.html'

    # def get_success_url(self):
    #     return reverse('/')
    success_url = reverse_lazy('workout_list_url')


class ExerciseDeleteView(DeleteView):
    model = Exercise
    template_name = 'diary/exercise_delete.html'
    success_url = reverse_lazy('workout_list_url')


class WorkoutDeleteView(DeleteView):
    model = Workout
    template_name = 'diary/workout_delete.html'
    success_url = reverse_lazy('workout_list_url')


class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutCreateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        view_name = 'exercise_list'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'slug': self.object.slug})


class ExerciseUpdateView(UpdateView):
    model = Exercise
    form_class = ExerciseCreateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        view_name = 'exercise_detail_url'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={
            'slug': self.object.slug,
            'author': self.object.author,
            'workout': self.object.workout,

        })


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
            'workout': self.object.exercise.workout,

        })


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