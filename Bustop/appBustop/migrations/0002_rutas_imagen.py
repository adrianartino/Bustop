# Generated by Django 3.0.5 on 2020-06-03 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBustop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutas',
            name='imagen',
            field=models.ImageField(null=True, upload_to='imagenesRutas'),
        ),
    ]
