# Generated by Django 3.1 on 2021-03-06 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='workouts.workout'),
        ),
    ]
