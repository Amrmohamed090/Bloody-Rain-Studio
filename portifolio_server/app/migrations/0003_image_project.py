# Generated by Django 5.0.4 on 2024-05-06 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_backgroundvideo_image_project_service_delete_video_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="app.project",
            ),
        ),
    ]
