# Generated by Django 3.0.2 on 2020-02-14 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0008_set_exercise'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='set',
            options={'ordering': ('-date',)},
        ),
    ]
