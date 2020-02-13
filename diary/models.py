from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
import datetime


class Category(models.Model):
    # Category means "Legs day", "Chest day"
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    # objects = models.Manager()

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    training_day = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='exercises')
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('exercise_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Exercise, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class TrainingDay(models.Model):
    # training contains exercises on a specific date
    slug = models.SlugField(max_length=20, unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    training_day = models.ManyToManyField(Exercise, related_name='training')

    def get_absolute_url(self):
        return reverse('training_detail_url', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     slug_data = str(TrainingCategory.slugself.date)
    #     self.slug = slugify()
    #     super(TrainingDay, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        date = datetime.datetime.now()
        self.slug = '{}, {}, {}, {}, {}, {},'.format(date.day, date.month, date.year, date.hour, date.minute,
                                                    date.second)
        super(TrainingDay, self).save()

    def __str__(self):
        return str(self.slug)


class Set(models.Model):
    set_number = models.IntegerField(default='', blank=True)
    exercise = models.ManyToManyField(Exercise, related_name='sets')
    weight = models.IntegerField(default='', blank=False)
    reps = models.IntegerField(default='', blank=False)
    date = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return 'Set #', self.set_number


# class Test(models.Model):
#     title = models.CharField(max_length=100)

