from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from datetime import date
from django.contrib.auth.views import LoginView, LogoutView


from .models import Exercise, Set, Workout
from django.views.generic import View, ListView, DeleteView, UpdateView, TemplateView, DetailView, CreateView
from .forms import *
from django.views.generic.dates import ArchiveIndexView


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


class WorkoutList(LoginRequiredMixin, ListView):
    model = Workout
    login_url = 'login_url'
    # LoginRequiredMixin
    # UserPassesTestMixin
    # def get_queryset(self):
    #     return super(WorkoutList, self).get_queryset().filter(author=self.request.user)

    # def test_func(self):
    #     all_obj = self.model.objects.all()
    #
    #     obj = self.model.objects.get
    #     return obj.author == self.request.user

    def get_queryset(self):
        return super(WorkoutList, self).get_queryset().filter(author=self.request.user)


class WorkoutDetail(View):
    def get(self, request, slug):
        workout = get_object_or_404(Workout, slug__iexact=slug)
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
            'exercise': exercise,
            'set_list': sets,
            'all_dates': all_dates,
            'all_sets_count': all_sets_count,
            # 'latest': latest,
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
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        form.save_m2m()
        return redirect('../')
    context = {
        'form': form
    }
    return render(request, 'diary/workout_create.html', context)


def exercise_create_view(request):
    form = ExerciseCreateForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        form.save_m2m()
        return redirect('../')
    context = {
        'form': form
    }
    return render(request, 'diary/exercise_create.html', context)


def set_create_view(request):
    form = SetCreateForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        form.save_m2m()
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


