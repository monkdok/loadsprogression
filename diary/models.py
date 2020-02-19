from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
import datetime


class Workout(models.Model):
    # Workout means "Legs day", "Chest day"

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('workout_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Workout, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    # workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercise_mm', )
    # sets = models.ManyToManyField('Set', related_name='exercises_mm', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    workout = models.ManyToManyField('Workout', related_name='exercise_mm', blank=True)

    def get_absolute_url(self):
        return reverse('exercise_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Exercise, self).save()

    def __str__(self):
        return self.title


class Set(models.Model):
    set_number = models.IntegerField(default='', blank=True)
    weight = models.IntegerField(default='', blank=False)
    reps = models.IntegerField(default='', blank=False)
    date = models.DateField(auto_now_add=True)
    exercise = models.ManyToManyField('Exercise', related_name='set_mm', blank=True)
    #
    # def save(self, *args, **kwargs):
    #     date = datetime.datetime.now()
    #     self.slug = '1 Set {}/{}/{}/{}/{}/{}'.format(
    #         date.day, date.month, date.year, date.hour, date.minute, date.second
    #     )
    #     super(Set, self).save()

    # class Meta:
    #     ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('sets_archive_url', kwargs={'slug': self.date})

    def __str__(self):
        # self.date = '{}/{}/{}'.format(date.day, date.month, date.year)
        w_r = '{}) {}x{}({})'.format(self.set_number, self.weight, self.reps, self.date)
        w_r = str(w_r)
        return w_r

