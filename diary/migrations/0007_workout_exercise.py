# Generated by Django 3.0.2 on 2020-03-15 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0006_auto_20200312_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='exercise',
            field=models.ManyToManyField(blank=True, related_name='exercise_ww', to='diary.Workout'),
        ),
    ]
