# Generated by Django 3.0.2 on 2020-03-12 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_auto_20200312_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='workout',
        ),
        migrations.AddField(
            model_name='exercise',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_mm', to='diary.Workout'),
        ),
    ]
