# Generated by Django 3.0.5 on 2020-05-12 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBustop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='nacimiento',
            field=models.DateField(),
        ),
    ]
