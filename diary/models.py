from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from slugify import slugify



class CommonInfo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, blank=False, unique=False)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True


class Workout(CommonInfo):
    workout_id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('exercise_list', kwargs={
            'slug': self.slug,
            'author': self.author,
        })

    def save(self, *args, **kwargs):
        custom_slug = '{}-{}-{}'.format(self.title, self.author, self.author.id)
        self.slug = slugify(custom_slug)
        super(Workout, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Exercise(CommonInfo):
    exercise_id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, related_name='exercise_mm', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('exercise_detail_url', kwargs={
            'slug': self.slug,
            'workout': self.workout.slug,
            'author': self.author,
        })

    def save(self, *args, **kwargs):
        custom_slug = '{}-{}-{}-{}'.format(self.workout, self.title, self.author, self.author.id)
        self.slug = slugify(custom_slug)
        super(Exercise, self).save()

    def __str__(self):
        return self.title


class Set(models.Model):
    # AUTH_USER_MODEL
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    set_number = models.PositiveIntegerField(default=0, blank=False)
    weight = models.PositiveIntegerField(default='', blank=True, null=True)
    reps = models.PositiveIntegerField(default='', blank=False)
    volume = models.PositiveIntegerField(default='', blank=True, null=True)
    # user_date = models.DateField(default=timezone.now, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, related_name='set_mm', blank=True, null=True)

    # def calculate_volume(self):
    #     volume = self.reps * self.weight
    #     return volume

    def save(self, *args, **kwargs):
        if self.weight is not None:
            self.volume = self.reps * self.weight
        else:
            self.volume = 0
        super(Set, self).save()

    # class Meta:
    #     ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('sets_archive_url', kwargs={'exercise': self.exercise, 'slug': self.date})

    def __str__(self):
        # self.date = '{}/{}/{}'.format(date.day, date.month, date.year)
        w_r = '{}) {}x{}({})'.format(self.set_number, self.weight, self.reps, self.date)
        w_r = str(w_r)
        return w_r
