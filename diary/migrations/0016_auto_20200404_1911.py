# Generated by Django 3.0.3 on 2020-04-04 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0015_auto_20200327_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='weight',
            field=models.PositiveIntegerField(blank=True, default=''),
        ),
    ]