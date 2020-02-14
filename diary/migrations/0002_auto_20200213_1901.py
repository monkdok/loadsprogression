# Generated by Django 3.0.2 on 2020-02-13 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='exercise',
        ),
        migrations.AddField(
            model_name='exercise',
            name='sets',
            field=models.ManyToManyField(related_name='exercises', to='diary.Set'),
        ),
        migrations.AddField(
            model_name='workout',
            name='exercise',
            field=models.ManyToManyField(related_name='workout_mm', to='diary.Exercise'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_mm', to='diary.Workout'),
        ),
    ]
