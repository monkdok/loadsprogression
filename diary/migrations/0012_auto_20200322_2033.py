# Generated by Django 3.0.2 on 2020-03-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0011_auto_20200320_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='set_number',
            field=models.IntegerField(blank=True, default='', max_length=2),
        ),
    ]
