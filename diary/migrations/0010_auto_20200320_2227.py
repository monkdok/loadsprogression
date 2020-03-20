# Generated by Django 3.0.3 on 2020-03-20 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0009_auto_20200320_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='exercise',
        ),
        migrations.AddField(
            model_name='set',
            name='exercise',
            field=models.ManyToManyField(blank=True, related_name='set_mm', to='diary.Exercise'),
        ),
    ]
