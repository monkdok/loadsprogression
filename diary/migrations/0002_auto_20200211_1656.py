# Generated by Django 3.0.3 on 2020-02-11 16:56

from django.db import migrations, models


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
            model_name='set',
            name='exercise',
            field=models.ManyToManyField(related_name='sets', to='diary.Exercise'),
        ),
        migrations.RemoveField(
            model_name='trainingday',
            name='training_day',
        ),
        migrations.AddField(
            model_name='trainingday',
            name='training_day',
            field=models.ManyToManyField(related_name='training', to='diary.Exercise'),
        ),
    ]
