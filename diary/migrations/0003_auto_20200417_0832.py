# Generated by Django 3.0.2 on 2020-04-17 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20200416_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='workout',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]