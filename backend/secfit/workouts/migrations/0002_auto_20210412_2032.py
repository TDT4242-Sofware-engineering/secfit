# Generated by Django 3.1 on 2021-04-12 20:32

from django.db import migrations, models
import workouts.models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RememberMe',
        ),
        migrations.AlterField(
            model_name='exercisefile',
            name='file',
            field=models.FileField(upload_to=workouts.models.exercise_directory_path, validators=[workouts.models.file_size]),
        ),
    ]
