# Generated by Django 3.0.3 on 2020-03-17 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_workout_exercise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='exercise',
        ),
    ]
