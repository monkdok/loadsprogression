from .utils import *


class WorkoutCreateView(ObjectCreateMixin, View):
    form = WorkoutCreateForm
    template = 'diary/btn_group_workout.html'


class WorkoutList(LoginRequiredMixin, ObjectListMixin, View):
    login_url = 'account_login'
    model = Workout
    form = WorkoutCreateForm()
    template = 'diary/workout_list.html'


class WorkoutUpdateView(ObjectUpdateMixin, View):
    model = Workout
    form = WorkoutCreateForm
    template = 'diary/btn_group_workout.html'


class WorkoutDeleteView(ObjectDeleteMixin, View):
    model = Workout


class ExerciseCreateView(ObjectCreateMixin, View):
    form = ExerciseCreateForm
    template = 'diary/btn_group_exercise.html'
    parent = Workout


class ExerciseList(LoginRequiredMixin, ObjectListMixin, View):
    login_url = 'account_login'
    model = Exercise
    parent = Workout
    template = 'diary/exercise_list.html'
    form = ExerciseCreateForm()


class ExerciseUpdateView(ObjectUpdateMixin, View):
    model = Exercise
    form = ExerciseCreateForm
    template = 'diary/btn_group_exercise.html'


class ExerciseDeleteView(ObjectDeleteMixin, View):
    model = Exercise


class SetCreateView(View):
    form = SetCreateForm
    template = 'diary/btn_group_set.html'
    parent = Exercise


class SetList(SetListMixin, View):
    model = Set
    template = 'diary/set_list.html'


class SetUpdateView(ObjectUpdateMixin, View):
    model = Set
    form = SetCreateForm
    template = 'diary/set_list.html'


class SetDeleteView(ObjectDeleteMixin, View):
    model = Set
    template = 'diary/set_list.html'
