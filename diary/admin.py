from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Workout)
# admin.site.register(Exercise)
# admin.site.register(Set)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'date')
    list_filter = ('date', 'workout')
    search_fields = ('title', 'date')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'


@admin.register(Set)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('set_number', 'weight', 'reps', 'date')
    list_filter = ('set_number', 'weight', 'exercise', 'date')
    search_fields = ('set_number', 'weight', 'exercise', 'date')
    raw_id_fields = ('exercise', )
    date_hierarchy = 'date'
    ordering = ('set_number', 'date')
